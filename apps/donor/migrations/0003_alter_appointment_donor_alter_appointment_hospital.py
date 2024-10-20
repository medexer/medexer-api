# Generated by Django 4.1.3 on 2023-04-15 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("donor", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="donor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="appointment_donor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="hospital",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="appointment_hospital",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
