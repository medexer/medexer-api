# Generated by Django 4.1.3 on 2023-04-17 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0008_complainthistory_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="complainthistory",
            old_name="status",
            new_name="updateType",
        ),
    ]
