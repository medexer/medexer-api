from django.urls import path
from . import views

urlpatterns = [
    path("centers/",views.center_list_viewset, name="centers"),
    path("center/<str:id>", views.center_detail_viewset, name="center-detail"),
    path("appointments/", views.hospital_appointment_viewset , name="hospital-appointments"),
    path("appointment/update/<int:pkid>", views.hospital_appointment_viewset, name="update-appointment-hospital"),
    path("inventory/fetch-all", views.hospital_inventory_viewset, name="fetch-all-inventory"),
    path("inventory/<str:bloodGroup>/update-units", views.inventory_item_detail_viewset, name="inventroy-item-update"),
    path("inventory/<str:bloodGroup>/activity/fetch-all", views.inventory_item_history_viewset , name="inventroy-item-activity"),
    path("notifications", views.hospital_notifications_viewset, name="hospital-notifiction"),
    path("notifications/<int:notificationId>/update", views.hospital_notifications_viewset, name="hospital-notifiction"),
    path("appointment/donor/donation-history/<int:donorId>", views.donor_donation_history_viewset, name="donor-donation-history"),
    path("complaints/fetch-all", views.hospital_complaint_viewset, name="fetch-complaints"),
    path("complaints/generate", views.hospital_complaint_viewset, name="create-complaint"),
    path("complaints/<int:complaintId>/update", views.hospital_complaint_viewset, name="update-complaint-status"),
    path("complaint/thread/<int:complaintId>/fetch-all", views.complaint_thread_viewset, name="fetch-complaint-thread"),
    path("complaint/thread/<int:complaintId>/reply", views.complaint_thread_viewset, name="reply-complaint-thread"),
]
