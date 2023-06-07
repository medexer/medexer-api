from django.urls import path
from . import views

urlpatterns = [
    path("appointments", views.donor_appointment_viewset, name="donor-appointments"),
    path("appointments/create", views.donor_appointment_viewset, name="donor-create-appointment"),
    path("appointments/<int:pkid>", views.donor_appointment_viewset, name="donor-appointment"),
    path("donation-centers", views.donation_centers_viewset, name="donation-centers"),
    path("donation-centers/geo-data/fetch-all", views.donation_centers_location_data_viewset, name="donation-centers-geo-data"),
    path("donation-centers/<int:centerId>", views.donation_center_detail_viewset, name="donation-center"),
    path("donation-centers/search", views.search_donation_centers_viewset, name="donation-centers-search"),
    path("contact-us", views.donor_contact_us_viewset, name="contact-us"),
    path("notifications", views.donor_notifications_viewset, name="donor-notification"),
    path("notifications/<int:notificationId>/update", views.donor_notifications_viewset, name="donor-notification"),
]
