from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import json

QUEUE_TYPE_NEW = 0
QUEUE_TYPE_LRN = 1
QUEUE_TYPE_REV = 2
QUEUE_TYPE_NEW_FAILED = 3 # when you get something as new but you fail it, so we don't remark it as using a new card

NEW_ADDED_EVERY_DAY = 5


class User(AbstractUser):
    new_cards_added_today = models.IntegerField(
        default=0
    )


class Card(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.CharField(max_length=800)
    back = models.CharField(max_length=800)
    date_next = models.DateField(default=datetime.date.today)
    time_next_today = models.DateTimeField(null=True,default=None)
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
