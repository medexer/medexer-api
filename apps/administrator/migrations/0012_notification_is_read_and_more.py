# Generated by Django 4.1.3 on 2023-04-17 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0011_notification_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="notification",
            name="notificationType",
            field=models.CharField(
                blank=True,
                choices=[
                    ("APPOINTMENT", "Appointment"),
                    ("HOSPITAL", "Hospital"),
                    ("DONATION", "Donation"),
                    ("ADMIN", "Admin"),
                    ("COMPLAINT", "Complaint"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
