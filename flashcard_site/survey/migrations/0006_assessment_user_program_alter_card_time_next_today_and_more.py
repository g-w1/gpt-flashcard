# Generated by Django 4.2.1 on 2023-05-24 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0005_reviewstat"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assessment",
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
                ("program", models.CharField(max_length=100)),
                ("questions", models.TextField()),
                ("correct_answers", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="program",
            field=models.CharField(default="TESTGROUP", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="card",
            name="time_next_today",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.CreateModel(
            name="AssessmentSubmission",
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
                ("supplied_answers", models.TextField()),
                ("at_beginning", models.BooleanField()),
                (
                    "assessment_belongs",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.assessment",
                    ),
                ),
                (
                    "user_belongs",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
