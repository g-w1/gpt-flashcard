# Generated by Django 4.2.1 on 2023-05-28 01:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0015_rename_use_flashcards_initialsurvey_use_flashcards_normally"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="time_for_final_assessment",
        ),
        migrations.RemoveField(
            model_name="user",
            name="time_for_initial_assessment",
        ),
        migrations.RemoveField(
            model_name="user",
            name="time_for_survey",
        ),
        migrations.AddField(
            model_name="initialsurvey",
            name="time_taken",
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
