# Generated by Django 4.2.1 on 2023-05-24 20:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0006_assessment_user_program_alter_card_time_next_today_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_used",
            field=models.DateField(default=datetime.date(2023, 5, 24)),
        ),
    ]
