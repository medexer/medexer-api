# Generated by Django 4.1.3 on 2023-06-03 12:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0019_notification_authortype'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='recipients',
            field=models.ManyToManyField(blank=True, related_name='notification_recipients', to=settings.AUTH_USER_MODEL),
        ),
    ]
