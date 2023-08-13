from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-pkid",)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "id",
        "pkid",
        "fullName",
        "hospitalName",
        "email",
        "is_active",
        "is_donor",
        "is_hospital",
        "is_administrator",
    ]
    
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "avatar",
                    "fullName",
                    "hospitalName",
                    "donorID",
                    "hospitalID",
                    "address",
                    "lga",
                    "state",
                    "postalCode",
                    "otp",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_administrator",
                    "is_donor",
                    "is_hospital",
                    "is_kyc_updated",
                    "is_approved",
                    # "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "fullName",
                    "email",
                    "hospitalName",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_donor",
                    "is_hospital",
                    "is_administrator",
                ),
            },
        ),
    )
