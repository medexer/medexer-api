# Generated by Django 4.1.3 on 2023-04-17 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0007_rename_compaintid_complaint_complaintid"),
    ]

    operations = [
        migrations.AddField(
            model_name="complainthistory",
            name="status",
            field=models.CharField(
                blank=True, default="THREAD", max_length=255, null=True
            ),
        ),
    ]
