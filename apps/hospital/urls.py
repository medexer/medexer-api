from django.urls import path
from . import views

urlpatterns = [
    path("inventory/", views.inventory_list_viewset , name="list-inventroy"),
    path("inventory/<str:id>", views.inventroy_detail_viewset, name="detail-inventroy"),
    path("centers/",views.center_list_viewset, name="centers"),
    path("center/<str:id>", views.center_detail_viewset, name="center-detail"),
    # path("appointments", views.appointment_viewset, name="appointments"),
    path("center_notification/",views.notification_viewset,name='center_notification'),
    path("appointments/", views.hospital_appointment_viewset , name="hospital-appointments"),
    path("appointment/<str:id>", views.update_hospital_appointment_viewset, name="update-appointment-hospital"),
    path("donor_activity/<str:id>", views.GetDonorActivity_viewset, name="donor-activity-hospital"),
    path("get_inventory/", views.getallhospital_inventroy_viewset, name="get-inventory"),
    
]
