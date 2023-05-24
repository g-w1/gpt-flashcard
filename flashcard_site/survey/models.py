from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import json

QUEUE_TYPE_NEW = 0
QUEUE_TYPE_LRN = 1
QUEUE_TYPE_REV = 2
QUEUE_TYPE_NEW_FAILED = 3  # when you get something as new but you fail it, so we don't remark it as using a new card

NEW_ADDED_EVERY_DAY = 5


class User(AbstractUser):
    new_cards_added_today = models.IntegerField(default=0)
    program = models.CharField(
        max_length=100
    )  # the school that the people belong to, we use this when fetching the assessment
    # this can definently be anonymized

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

    def review_missed(self):
        pass
        # TODO implement that if dtime_now > date_scheduled_before then return true because they are on different days


class Assessment(models.Model):
    program = models.CharField(
        max_length=100
    )  # the school that the people belong to, we use this when fetching the assessment
    questions = (
        models.TextField()
    )  # this is just some json array schema like this [{'question': 'What is your favorite color?', 'answers': ['Red', 'Blue', 'Green']}, ...]
    correct_answers = (
        models.TextField()
    )  # an array with the correct indexes [2, ...] means green is fav color


class AssessmentSubmission(models.Model):
    user_belongs = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # TODO look into if we will be deleting users; I don't think so so this is fine
    # user_belongs.program == assessment_belongs.program # TODO make this an assertion
    assessment_belongs = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    supplied_answers = (
        models.TextField()
    )  # this is just some json arary schema like this [2, ...] where the number is just the index in the answer of the corresponding question.
    # so in this case, the user would have answered 'Green' (index 2) to the first question. len(anwsers) must equal len(asessment.questions)
    at_beginning = (
        models.BooleanField()
    )  # we want to test the user on the same set of questions at the end
