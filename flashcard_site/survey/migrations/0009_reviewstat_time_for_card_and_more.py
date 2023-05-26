# Generated by Django 4.2.1 on 2023-05-25 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0008_alter_user_last_used"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewstat",
            name="time_for_card",
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="time_for_final_assessment",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="time_for_initial_assessment",
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="time_for_writing",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="time_on_survey",
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
    ]