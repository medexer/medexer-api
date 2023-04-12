from django.urls import path
from . import views

urlpatterns = [
    path("inventroy/", views.inventory_list_viewset , name="list-inventroy"),
    # path("appointments/<str:id>", views.donor_detail_viewset, name="donor-appointment"),
    
]
