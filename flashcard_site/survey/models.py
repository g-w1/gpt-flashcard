from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import json

CARD_TYPE_NEW = 0
CARD_TYPE_LRN = 1
CARD_TYPE_REV = 2
CARD_TYPE_RLN = 3

QUEUE_TYPE_NEW = 0
QUEUE_TYPE_LRN = 1
QUEUE_TYPE_REV = 2

NEW_ADDED_EVERY_DAY = 5


class User(AbstractUser):
    new_cards_added_today = models.IntegerField(
        default=NEW_ADDED_EVERY_DAY
    )  # think of better way to do this


class Card(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.CharField(max_length=800)
    back = models.CharField(max_length=800)
    date_next = models.DateField(default=datetime.date.today)
    date_next.editable = True
    easiness = models.FloatField(
        default=2.5
    )  # Initial value for easiness factor in SM2 algorithm is 2.5
    interval = models.IntegerField(default=1)  # Initial interval is 1 day
    repetitions = models.IntegerField(
        default=0
    )  # Initially, the card has not been reviewed, so repetitions is 0
    card_type = models.IntegerField(default=CARD_TYPE_NEW)  # Initially, the card is new
    queue_type = models.IntegerField(default=QUEUE_TYPE_NEW)

    def __str__(self):
        return f"{self.front}/{self.back}/next: {self.date_next}"
