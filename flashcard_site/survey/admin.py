from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Card, User
admin.site.register(Card)
admin.site.register(User, UserAdmin)
