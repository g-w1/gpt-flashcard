from django import forms
from .models import InitialSurvey, User, Card
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class InitialSurveyForm(forms.ModelForm):
    age = forms.IntegerField(label="Your Age")
    occupation = forms.ChoiceField(
        choices=InitialSurvey.OCCUPATION_CHOICES,
        initial="student",
        label="Your Occupation",
        help_text="Please select your current occupation.",
    )
    used_flashcards = forms.ChoiceField(
        choices=InitialSurvey.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        label="Have you ever used flashcards?",
        help_text="Please select whether you have ever used flashcards to study.",
    )
    use_flashcards_normally = forms.ChoiceField(
        required=False,
        choices=InitialSurvey.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        label="Do you normally use flashcards?",
        help_text="Please select whether you normally use flashcards to study. This field is optional if you are not a student.",
    )
    flashcard_skill = forms.ChoiceField(
        choices=InitialSurvey.LIKERT_SCALE_CHOICES,
        widget=forms.RadioSelect,  # TODO change the css
        label="Rate your skill at creating flashcards",
        help_text="Please rate your skill at creating flashcards, on a scale from 1 to 5.",
    )

    class Meta:
        model = InitialSurvey
        exclude = ["user", "time_taken"]


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email", "survey_group")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["front", "back"]
