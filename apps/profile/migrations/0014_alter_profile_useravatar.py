# Generated by Django 4.0.5 on 2023-07-05 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0013_alter_profile_useravatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userAvatar',
            field=models.ImageField(blank=True, default='user-avatar/avatar__1_ranrck.png', max_length=1000, null=True, upload_to='Medexer-API/media/user-avatar/'),
        ),
    ]
