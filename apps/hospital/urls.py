from django.urls import path
from . import views

urlpatterns = [
    path("donors/<str:query>/search", views.donor_search_viewset , name="hospital-search-donors"),
    path("appointments/", views.hospital_appointment_viewset , name="hospital-appointments"),
    path("appointment/update/<int:pkid>", views.hospital_appointment_viewset, name="update-appointment-hospital"),
    path("appointment/process/<int:pkid>", views.hospital_process_donation_viewset, name="process-successful-donation"),
    path("appointment/payment/verify/<str:reference>", views.hospital_donation_payment_viewset, name="verify-donation-payment"),
    path("appointment/payment/initialize/<int:donation>", views.hospital_donation_payment_viewset, name="process-donation-payment"),
    path("inventory/fetch-all", views.hospital_inventory_viewset, name="fetch-all-inventory"),
    path("inventory/<str:bloodGroup>/fetch-all", views.hospital_inventory_item_viewset, name="fetch-all-inventory-items"),
    path("inventory/<int:inventoryItem>/update-units", views.inventory_item_detail_viewset, name="inventroy-item-update"),
    path("inventory/<str:bloodGroup>/activity/fetch-all", views.inventory_item_history_viewset , name="inventroy-item-activity"),
    path("notifications", views.hospital_notifications_viewset, name="hospital-notification"),
    path("notifications/<int:notificationId>/update", views.hospital_notifications_viewset, name="hospital-notification"),
    path("appointment/donor/donation-history/<int:donorId>", views.donor_donation_history_viewset, name="donor-donation-history"),
    path("complaints/fetch-all", views.hospital_complaint_viewset, name="fetch-complaints"),
    path("complaints/generate", views.hospital_complaint_viewset, name="create-complaint"),
    path("complaints/<int:complaintId>/update", views.hospital_complaint_viewset, name="update-complaint-status"),
    path("complaint/thread/<int:complaintId>/fetch-all", views.complaint_thread_viewset, name="fetch-complaint-thread"),
    path("complaint/thread/<int:complaintId>/reply", views.complaint_thread_viewset, name="reply-complaint-thread"),
]
