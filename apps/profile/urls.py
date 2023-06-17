from django.urls import path
from . import views


urlpatterns = [
    path('hospital/fetch', views.hospital_profile_viewset, name="hospital-fetch-profile"),
    path('hospital/update', views.hospital_profile_viewset, name="hospital-update-profile"),
]
