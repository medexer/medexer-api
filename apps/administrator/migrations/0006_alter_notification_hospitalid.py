# Generated by Django 4.1.3 on 2023-04-11 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0005_alter_complaint_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='hospitalID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
