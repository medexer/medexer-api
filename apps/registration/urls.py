from django.urls import path
from . import views


urlpatterns = [
    path("donor/kyc-capture", views.donor_kyc_viewset, name="donor-kyc-capture"),
    path("hospital/kyb-capture", views.hospital_kyb_viewset, name="hospital-kyb-capture"),
]
