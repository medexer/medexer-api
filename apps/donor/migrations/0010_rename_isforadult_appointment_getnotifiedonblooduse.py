# Generated by Django 4.0.5 on 2023-07-06 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0009_appointment_isforadult_appointment_visitrecipient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='isForAdult',
            new_name='getNotifiedOnBloodUse',
        ),
    ]
