from django.urls import path
from . import views

urlpatterns = [
    path("centers/",views.center_list_viewset, name="centers"),
    path("center/<str:id>", views.center_detail_viewset, name="center-detail"),
    path("center_notification/",views.notification_viewset,name='center_notification'),
    path("appointments/", views.hospital_appointment_viewset , name="hospital-appointments"),
    path("appointment/update/<int:pkid>", views.hospital_appointment_viewset, name="update-appointment-hospital"),
    path("inventory/fetch-all", views.hospital_inventory_viewset, name="fetch-all-inventory"),
    path("inventory/<str:bloodGroup>/update-units", views.inventory_item_detail_viewset, name="inventroy-item-update"),
    path("inventory/<str:bloodGroup>/activity/fetch-all", views.inventory_item_history_viewset , name="inventroy-item-activity"),
    path("appointment/donor/donation-history/<int:donorId>", views.donor_donation_history_viewset, name="donor-donation-history"),
    path("getnotifications/", views.hospital_notification_viewset, name="hospital-notifiction"),
]
