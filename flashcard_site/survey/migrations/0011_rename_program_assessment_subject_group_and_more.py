# Generated by Django 4.2.1 on 2023-05-26 15:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0010_rename_time_on_survey_user_time_for_survey"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assessment",
            old_name="program",
            new_name="subject_group",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="program",
            new_name="subject_group",
        ),
    ]