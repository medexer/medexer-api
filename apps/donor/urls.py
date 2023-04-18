from django.urls import path
from . import views

urlpatterns = [
    path("appointments", views.donor_create_list_viewset, name="donor-appointments"),
    path("appointments/create", views.donor_appointment_viewset, name="donor-create-appointment"),
    path("appointments/<int:pkid>", views.donor_appointment_viewset, name="donor-appointment"),
    path("donation-centers", views.donation_centers_viewset, name="donation-centers"),
    path("donation-centers/<int:centerId>", views.donation_center_detail_viewset, name="donation-center"),
]
