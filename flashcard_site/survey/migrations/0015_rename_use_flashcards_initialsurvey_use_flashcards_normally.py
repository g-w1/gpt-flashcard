# Generated by Django 4.2.1 on 2023-05-28 01:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0014_initialsurvey"),
    ]

    operations = [
        migrations.RenameField(
            model_name="initialsurvey",
            old_name="use_flashcards",
            new_name="use_flashcards_normally",
        ),
    ]
