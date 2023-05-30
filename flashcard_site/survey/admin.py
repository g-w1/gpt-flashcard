from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    Card,
    User,
    ReviewStat,
    Assessment,
    AssessmentSubmission,
    InitialSurvey,
    SurveyGroup,
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("last_login",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_used",
                    "date_final_opens",
                )
            },
        ),
        (
            "Custom Fields",
            {
                "fields": (
                    "new_cards_added_today",
                    "survey_group",
                    "experiment_group",
                    "time_for_writing",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Card)
admin.site.register(ReviewStat)
admin.site.register(Assessment)
admin.site.register(AssessmentSubmission)
admin.site.register(InitialSurvey)
admin.site.register(SurveyGroup)
admin.site.register(User, CustomUserAdmin)
