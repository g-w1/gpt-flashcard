from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
import json

QUEUE_TYPE_NEW = 0
QUEUE_TYPE_LRN = 1
QUEUE_TYPE_REV = 2
QUEUE_TYPE_NEW_FAILED = 3  # when you get something as new but you fail it, so we don't remark it as using a new card

NEW_ADDED_EVERY_DAY = 5

class SurveyGroup(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """Manager for User Profiles"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    new_cards_added_today = models.IntegerField(default=0)
    survey_group = models.ForeignKey(SurveyGroup, on_delete=models.CASCADE)
    last_used = models.DateField(default=datetime.date.today)
    date_joined = models.DateTimeField(auto_now_add=True)
    time_for_writing = models.IntegerField(null=True, blank=True)
    date_final_opens = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Card(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.CharField(max_length=800)
    back = models.CharField(max_length=800)
    date_next = models.DateField(default=datetime.date.today)
    time_next_today = models.DateTimeField(null=True, blank=True, default=None)
    date_next.editable = True
    easiness = models.FloatField(
        default=2.5
    )  # Initial value for easiness factor in SM2 algorithm is 2.5
    interval = models.IntegerField(default=0)
    repetitions = models.IntegerField(
        default=0
    )  # Initially, the card has not been reviewed, so repetitions is 0
    queue_type = models.IntegerField(default=QUEUE_TYPE_NEW)

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
    survey_group = models.ForeignKey(SurveyGroup, on_delete=models.CASCADE)  # the school that the people belong to, we use this when fetching the assessment
    questions = (
        models.TextField()
    )  # this is just some json array schema like this [{"question": "What is your favorite color?", "answers": ["Red", "Blue", "Green"]}, ...]
    correct_answers = (
        models.TextField()
    )  # an array with the correct indexes [2, ...] means green is fav color


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
        ('student', 'Student'),
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
    ]
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LIKERT_SCALE_CHOICES = [(i, i) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)
    used_flashcards = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    use_flashcards_normally = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, null=True)
    flashcard_skill = models.IntegerField(choices=LIKERT_SCALE_CHOICES)
    time_taken = models.PositiveIntegerField()
