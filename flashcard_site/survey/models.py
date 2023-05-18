from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.

class User(AbstractUser):
	pass
class Card(models.Model):
    belongs = models.ForeignKey(User, on_delete=models.CASCADE)
    front = models.CharField(max_length=800)
    back = models.CharField(max_length=800)
    date_next = models.DateField(auto_now_add=True)
    date_next.editable=True

    def __str__(self):
        return f'{self.front}/{self.back}/next: {self.date_next}'
