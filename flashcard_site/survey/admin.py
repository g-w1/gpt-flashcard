from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Card, User, ReviewStat, Assessment, AssessmentSubmission, InitialSurvey


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            "Custom Fields",  # group heading of your choice; set to None for a blank space instead of a header
            {
                "fields": ("new_cards_added_today","subject_group","last_used","time_for_writing",),
            },
        ),
    )



admin.site.register(Card)
admin.site.register(ReviewStat)
admin.site.register(Assessment)
admin.site.register(AssessmentSubmission)
admin.site.register(InitialSurvey)
admin.site.register(User, CustomUserAdmin)

