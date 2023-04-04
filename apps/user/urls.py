from django.urls import path
from . import views


urlpatterns = [
    path("auth", views.geeks_view, name="donor-template"),
    path("auth/donor/signup", views.donor_signup_viewset, name="donor-signup"),
    path("auth/donor/signin", views.donor_signin_viewset, name="donor-signin"),
    path("auth/donor/forgot-password", views.donor_forgotpassword_viewset, name="donor-forgot-password"),
    path("auth/donor/reset-password", views.donor_resetpassword_viewset, name="donor-reset-password"),
    path("auth/hospital/signup", views.hospital_signup_viewset, name="hospital-signup"),
    path("auth/hospital/signin", views.hospital_signin_viewset, name="hospital-signin"),
]
