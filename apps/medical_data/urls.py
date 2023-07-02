from django.urls import path
from . import views


urlpatterns = [
    path("donor/medical-history/fetch-all", views.donor_medical_history_viewset, name="donor-medical-history"),
]
