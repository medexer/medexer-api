# Generated by Django 4.2.1 on 2023-06-29 01:52

import apps.common.media
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_remove_profile_bloodgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hospitalImage',
            field=models.ImageField(blank=True, default='/images/profile/hospital__1.jpg', null=True, upload_to=apps.common.media.hospital_image_path),
        ),
    ]
