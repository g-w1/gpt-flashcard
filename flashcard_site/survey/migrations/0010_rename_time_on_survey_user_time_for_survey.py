# Generated by Django 4.2.1 on 2023-05-26 15:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0009_reviewstat_time_for_card_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="time_on_survey",
            new_name="time_for_survey",
        ),
    ]
