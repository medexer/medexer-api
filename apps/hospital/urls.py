from django.urls import path
from . import views

urlpatterns = [
    path("inventroy/", views.inventory_list_viewset , name="list-inventroy"),
    path("inventroy/<str:id>", views.inventroy_detail_viewset, name="detail-inventroy"),
    path("centers/",views.center_list_viewset, name="centers")
    
]
