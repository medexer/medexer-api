# Generated by Django 4.1.3 on 2023-04-15 00:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Inventory",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("bloodGroup", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "bloodUnits",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                ("hospitalID", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "verbose_name_plural": "Inventory",
            },
        ),
        migrations.CreateModel(
            name="InventoryActivity",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("activity", models.CharField(blank=True, max_length=255, null=True)),
                ("hospitalID", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "verbose_name_plural": "Inventory Activities",
            },
        ),
    ]
