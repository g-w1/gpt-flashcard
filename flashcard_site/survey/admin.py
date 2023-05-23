from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Card, User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            "Custom Fields",  # group heading of your choice; set to None for a blank space instead of a header
            {
                "fields": ("new_cards_added_today",),
            },
        ),
    )


admin.site.register(Card)
admin.site.register(User, CustomUserAdmin)
