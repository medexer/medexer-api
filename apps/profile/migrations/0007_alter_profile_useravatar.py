# Generated by Django 4.2.1 on 2023-07-01 02:12

import apps.common.media
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_profile_gender_profile_nationality_profile_religion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userAvatar',
            field=models.ImageField(blank=True, default='/images/profile/avatar__1.png', null=True, upload_to=apps.common.media.avatar_path),
        ),
    ]
