# Generated by Django 4.1.3 on 2023-04-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="donorID",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Donor ID",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Email Address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="hospitalID",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Hospital ID",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="hospitalName",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Hospital Name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="location",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Location"
            ),
        ),
    ]
