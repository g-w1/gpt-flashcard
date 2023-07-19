from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.core import mail
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.template.loader import render_to_string
from django.urls import reverse
import datetime
import json

QUEUE_TYPE_NEW = 0
QUEUE_TYPE_LRN = 1
QUEUE_TYPE_REV = 2
QUEUE_TYPE_NEW_FAILED = 3  # when you get something as new but you fail it, so we don't remark it as using a new card

NEW_ADDED_EVERY_DAY = 15


class SurveyGroup(models.Model):
    name = models.CharField(max_length=100)
    cards_per_week = models.PositiveIntegerField(default=45)
    topics_to_make = models.TextField()  # json array of 5 arrays of strings
    ai_cards = models.TextField()  # json of [{'question': Q, 'answer': A}]

    def get_topic_to_make(self, days_passed):
        topics_parsed = json.loads(self.topics_to_make)
        week = days_passed // 7
        if week > 4:
            week = 4
        return topics_parsed[week]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            ttm = json.loads(self.topics_to_make)
            aic = json.loads(self.ai_cards)
            assert type(ttm) == list
            assert len(ttm) == 5
            assert type(aic) == list
        except:
            raise ValidationError(
                "SurveyGroup topics_to_make or ai_cards was not valid JSON"
            )
        super(SurveyGroup, self).save(*args, **kwargs)


class UserManager(BaseUserManager):
    """Manager for User Profiles"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.time_for_writing = None
        user.date_final_opens = timezone.localdate() + datetime.timedelta(
            7 * 4
        )  # TODO make it not 4 weeks
        user.set_password(password)
        survey_group, created = SurveyGroup.objects.get_or_create(
            name="DEFAULT"
        )  # TODO, we need to immediately change it from default
        user.survey_group = survey_group
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        survey_group, created = SurveyGroup.objects.get_or_create(name="ADMIN")
        user.survey_group = survey_group
        user.save(using=self._db)

        return user


EXPERIMENT_GROUP_WRITING = 1
EXPERIMENT_GROUP_AI = 2


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    new_cards_added_today = models.IntegerField(default=0)
    survey_group = models.ForeignKey(SurveyGroup, on_delete=models.CASCADE)
    experiment_group = models.IntegerField()
    last_used = models.DateField(default=timezone.localtime)
    date_joined = models.DateTimeField(auto_now_add=True)
    time_for_writing = models.IntegerField(null=True, blank=True)
    date_final_opens = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def needs_to_take_survey(self):
        return not InitialSurvey.objects.filter(user=self).exists()

    @property
    def needs_to_take_initial_assessment(self):
        return not AssessmentSubmission.objects.filter(
            user_belongs=self,
            at_beginning=True,
        ).exists()

    @property
    def needs_to_take_final_assessment(self):
        doesnt_exist = not AssessmentSubmission.objects.filter(
            user_belongs=self,
            at_beginning=True,
        ).exists()
        return self.final_assessment_is_due() and doesnt_exist

    @property
    def num_cards_to_do_today(self):
        cards_for_today = Card.objects.filter(
            Q(belongs=self)
            & Q(suspended=False)
            & Q(date_next__lte=timezone.localtime())
            & (
                Q(time_next_today__lte=timezone.localtime())
                | Q(time_next_today__isnull=True)
            )
        )
        new_cards_num = cards_for_today.filter(queue_type=QUEUE_TYPE_NEW).count()
        possible_new_cards_num = min(
            new_cards_num, NEW_ADDED_EVERY_DAY - self.new_cards_added_today
        )
        return cards_for_today.count() - new_cards_num + possible_new_cards_num

    @property
    def num_cards_to_add_today(self):
        return (
            NEW_ADDED_EVERY_DAY
            - Card.objects.filter(
                created=timezone.localdate(),
                belongs=self,
            ).count()
        )

    def final_assessment_is_due(self):
        return self.date_final_opens <= timezone.localdate()

    @property
    def topics_to_make(self):
        days_passed = (timezone.localtime() - self.date_joined).days
        return self.survey_group.get_topic_to_make(days_passed)

    def send_daily_reminder(self):
        print(f"send_daily_reminder for {self.email}")
        from_email = "Flashcard Reminder <reminder@flashcard-study.org>"
        to = [self.email]
        if self.final_assessment_is_due():
            if self.needs_to_take_final_assessment:
                subject = "Complete Your Final Check-In"
                html_message = render_to_string("survey/do_final.html", {})
                plain_message = strip_tags(html_message)
                print(f"sending reminder for {self.email} ...")
                mail.send_mail(
                    subject, plain_message, from_email, to, html_message=html_message
                )
            else:
                return
        else:
            num_cards_to_do_today = self.num_cards_to_do_today
            if num_cards_to_do_today == 0:
                return
            subject = "Review Your Flashcards Today"
            html_message = render_to_string(
                "survey/daily_reminder.html", {"num_cards": num_cards_to_do_today}
            )
            plain_message = strip_tags(html_message)
            print(f"sending reminder for {self.email} ...")
            mail.send_mail(
                subject, plain_message, from_email, to, html_message=html_message
            )

    @staticmethod
    def send_daily_reminders():
        print("called send_daily_reminders")
        users = list(User.objects.all())
        for user in users:
            user.send_daily_reminder()

    def send_registration_email(self):
        subject = "Flashcard Study Info"
        from_email = "Flashcard Reminder <reminder@flashcard-study.org>"
        to = [self.email]
        html_message = render_to_string("survey/on_signup.html", {})
        plain_message = strip_tags(html_message)
        mail.send_mail(
            subject, plain_message, from_email, to, html_message=html_message
        )

    def add_ai_cards_from_survey_group(self):
        cards = json.loads(self.survey_group.ai_cards)
        for card in cards:
            q = card["question"]
            a = card["answer"]
            c = Card(belongs=self, front=q, back=a)
            c.save()


class Card(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
    date_next = models.DateField(default=timezone.localdate)
    date_next.editable = True
    time_next_today = models.DateTimeField(null=True, blank=True, default=None)
    easiness = models.FloatField(
        default=2.5
    )  # Initial value for easiness factor in SM2 algorithm is 2.5
    interval = models.IntegerField(default=0)
    repetitions = models.IntegerField(
        default=0
    )  # Initially, the card has not been reviewed, so repetitions is 0
    queue_type = models.IntegerField(default=QUEUE_TYPE_NEW)
    created = models.DateField(auto_now_add=True)  # why not showing up in admin
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.front}/{self.back}/next: {self.date_next}"


# happens every time a user submits a card
class ReviewStat(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    dtime_now = models.DateTimeField()
    quality = models.IntegerField()
    interval_before = models.IntegerField()
    interval_after = models.IntegerField()
    easiness_before = models.FloatField()
    easiness_after = models.FloatField()
    date_scheduled_before = models.DateField()
    date_scheduled_after = models.DateField()
    time_for_card = models.IntegerField()

    def review_missed(self):
        if self.dtime_now.date() > self.date_scheduled_before:
            return True
        return False

    def __str__(self):
        return f"{self.card.front}|s={self.time_for_card}|Q={self.quality}"


class Assessment(models.Model):
    survey_group = models.ForeignKey(
        SurveyGroup, on_delete=models.CASCADE
    )  # the school that the people belong to, we use this when fetching the assessment
    questions_start = (
        models.TextField()
    )  # this is just some json array schema like this [{"question": "What is your favorite color?", "answers": ["Red", "Blue", "Green"]}, ...]
    correct_answers_start = (
        models.TextField()
    )  # an array with the correct indexes [2, ...] means green is fav color
    questions_end = models.TextField()
    correct_answers_end = models.TextField()


class AssessmentSubmission(models.Model):
    user_belongs = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # TODO look into if we will be deleting users; I don't think so so this is fine
    # user_belongs.survey_group == assessment_belongs.survey_group # TODO make this an assertion
    assessment_belongs = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    supplied_answers = (
        models.TextField()
    )  # this is just some json arary schema like this [2, ...] where the number is just the index in the answer of the corresponding question.
    # so in this case, the user would have answered 'Green' (index 2) to the first question. len(anwsers) must equal len(asessment.questions)
    at_beginning = models.BooleanField()
    time_taken = models.PositiveIntegerField()


class InitialSurvey(models.Model):
    OCCUPATION_CHOICES = [
        ("student", "Student"),
        ("employed", "Employed"),
        ("unemployed", "Unemployed"),
        ("retired", "Retired"),
    ]
    STUDY_OUTSIDE_CHOICES = [
        ("<30m", "Studying for less than 30 minutes outside of school every week"),
        (
            "1-2h",
            "Studying for 1-2 hours outside of school every week",
        ),
        ("3-4", "Studying for 3-4 hours outside of school every week"),
        ("5", "Studying for more than 5 hours outside of school every week"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)
    study_outside = models.CharField(
        max_length=100, choices=STUDY_OUTSIDE_CHOICES, default="<30m"
    )
    HOW_MANY_TIMES_CHOICES = [
        ("0", "0"),
        ("1-2", "1-2"),
        ("3-5", "3-5"),
        ("5-10", "5-10"),
        ("more than 10", "more than 10"),
    ]
    how_many_times_used_flashcards = models.CharField(
        max_length=100, choices=HOW_MANY_TIMES_CHOICES, default="3-5"
    )
    time_taken = models.PositiveIntegerField()
