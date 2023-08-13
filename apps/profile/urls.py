from django.urls import path
from . import views


urlpatterns = [
    path('hospital/fetch', views.hospital_profile_viewset, name="hospital-fetch-profile"),
    path('hospital/update', views.hospital_profile_viewset, name="hospital-update-profile"),
    path('hospital/media/update', views.hospital_media_viewset, name="hospital-update-media"),
    path('donor/update-location', views.donor_profile_location_viewset, name="donor-update-location"),
]
