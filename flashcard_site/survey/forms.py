from django import forms
from .models import InitialSurvey, User, Card, SurveyGroup
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class InitialSurveyForm(forms.ModelForm):
    age = forms.IntegerField(label="Your Age")
    occupation = forms.ChoiceField(
        choices=InitialSurvey.OCCUPATION_CHOICES,
        initial="student",
        label="Your Occupation",
    )
    used_flashcards = forms.ChoiceField(
        choices=InitialSurvey.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        label="Have you ever used flashcards to study?",
    )
    use_flashcards_normally = forms.ChoiceField(
        required=False,
        choices=InitialSurvey.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        label="Do you normally use flashcards to study?",
    )
    flashcard_skill = forms.ChoiceField(
        choices=InitialSurvey.LIKERT_SCALE_CHOICES,
        widget=forms.RadioSelect,  # TODO change the css
        label="Rate your skill at creating flashcards",
    )
    study_outside = forms.ChoiceField(
    	choices=InitialSurvey.STUDY_OUTSIDE_CHOICES,
    	label="How much do you plan to study outside of school (not including this study)?"
    )


    class Meta:
        model = InitialSurvey
        exclude = ["user", "time_taken"]


class CustomUserCreationForm(UserCreationForm):
    survey_group = forms.CharField()

    class Meta(UserCreationForm):
        model = User
        fields = ("email", "survey_group")

    def clean_survey_group(self):
        survey_group_name = self.cleaned_data["survey_group"]
        try:
            survey_group = SurveyGroup.objects.get(name=survey_group_name)
        except SurveyGroup.DoesNotExist:
            raise forms.ValidationError(
                "The group does not exist, please enter a valid group code."
            )
        return survey_group


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["front"].widget = forms.TextInput()
        self.fields["back"].widget = forms.TextInput()
