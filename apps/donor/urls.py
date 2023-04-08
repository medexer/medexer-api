from django.urls import path
from . import views

urlpatterns = [
    path("appointments/", views.donor_create_list_viewset, name="donor-appointments"),
    path("appointments/<str:id>", views.donor_detail_viewset, name="donor-appointment"),
    
]
