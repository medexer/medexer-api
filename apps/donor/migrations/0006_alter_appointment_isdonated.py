# Generated by Django 4.1.3 on 2023-04-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0005_appointment_isdonated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='isDonated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
