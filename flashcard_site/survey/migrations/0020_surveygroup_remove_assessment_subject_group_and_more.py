# Generated by Django 4.2.1 on 2023-05-29 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0019_user_date_joined"),
    ]

    operations = [
        migrations.CreateModel(
            name="SurveyGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="assessment",
            name="subject_group",
        ),
        migrations.RemoveField(
            model_name="user",
            name="subject_group",
        ),
        migrations.AddField(
            model_name="assessment",
            name="survey_group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="survey.surveygroup",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="survey_group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="survey.surveygroup",
            ),
        ),
    ]
