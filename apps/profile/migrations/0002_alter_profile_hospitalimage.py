# Generated by Django 4.1.4 on 2023-06-19 09:46

import apps.common.media
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hospitalImage',
            field=models.ImageField(blank=True, default='/images/profile/hospital__1', null=True, upload_to=apps.common.media.hospital_image_path),
        ),
    ]
