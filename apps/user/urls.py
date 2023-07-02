from django.urls import path
from . import views


urlpatterns = [
    path("auth", views.geeks_view, name="donor-template"),
    path("auth/administrator/signin", views.admin_signin_viewset, name="admin-signin"),
    path("auth/administrator/update-profile", views.admin_profile_update_viewset, name="admin-profile-update"),
    path("auth/administrator/update-password", views.admin_password_update_viewset, name="admin-password-update"),
    path("auth/donor/signup", views.donor_signup_viewset, name="donor-signup"),
    path("auth/donor/signin", views.donor_signin_viewset, name="donor-signin"),
    path("auth/donor/signout", views.donor_signout_viewset, name="donor-signout"),
    path("auth/donor/delete-account", views.donor_delete_account_viewset, name="donor-delete-account"),
    path("auth/donor/google-signin", views.donor_googlesignin_viewset, name="donor-google-signin"),
    path("auth/donor/forgot-password", views.donor_forgotpassword_viewset, name="donor-forgot-password"),
    path("auth/donor/reset-password", views.donor_resetpassword_viewset, name="donor-reset-password"),
    path("auth/donor/update-profile", views.donor_update_profile_viewset, name="donor-update-profile"),
    path("auth/donor/update-signup-profile", views.donor_update_signup_profile_viewset, name="donor-update-signup-profile"),
    path("auth/donor/update-google-signin-profile", views.donor_update_profile_with_google_signin_viewset, name="donor-update-google-signin-profile"),
    path("auth/hospital/signup", views.hospital_signup_viewset, name="hospital-signup"),
    path("auth/hospital/signin", views.hospital_signin_viewset, name="hospital-signin"),
    path("auth/hospital/update-profile", views.update_hospital_viewset, name="update-hospital-profile"),
]
