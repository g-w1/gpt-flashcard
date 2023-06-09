# Generated by Django 4.2.1 on 2023-05-28 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0013_user_date_final_opens"),
    ]

    operations = [
        migrations.CreateModel(
            name="InitialSurvey",
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
                ("age", models.PositiveIntegerField()),
                (
                    "occupation",
                    models.CharField(
                        choices=[
                            ("student", "Student"),
                            ("employed", "Employed"),
                            ("unemployed", "Unemployed"),
                            ("retired", "Retired"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "used_flashcards",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No")], max_length=3
                    ),
                ),
                (
                    "use_flashcards",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No")],
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    "flashcard_skill",
                    models.IntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
