# Generated by Django 4.1.3 on 2023-04-15 00:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
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
                (
                    "fullName",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Full Name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Email Address",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Location"
                    ),
                ),
                (
                    "hospitalName",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Hospital Name",
                    ),
                ),
                (
                    "donorID",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Donor ID",
                    ),
                ),
                (
                    "hospitalID",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Hospital ID",
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_donor", models.BooleanField(default=False)),
                ("is_hospital", models.BooleanField(default=False)),
                ("is_administrator", models.BooleanField(default=False)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "otp",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("is_kyc_updated", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
    ]
