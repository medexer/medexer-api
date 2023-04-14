from django.urls import path
from . import views

urlpatterns = [
    path("inventory/", views.inventory_list_viewset , name="list-inventroy"),
    path("inventory/<str:id>", views.inventroy_detail_viewset, name="detail-inventroy"),
    path("centers/",views.center_list_viewset, name="centers"),
    path("center/<str:id>", views.center_detail_viewset, name="center-detail"),
    path("appointments", views.appointment_viewset, name="appointments"),
]
