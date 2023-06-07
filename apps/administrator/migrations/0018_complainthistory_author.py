# Generated by Django 4.1.3 on 2023-06-03 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0017_integration_accesskey'),
    ]

    operations = [
        migrations.AddField(
            model_name='complainthistory',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaint_history_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
