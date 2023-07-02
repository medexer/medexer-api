from django.urls import path
from . import views


urlpatterns = [
    path("donor/medical-history/fetch-all", views.donor_medical_history_viewset, name="donor-medical-history"),
    path("hospital/donors/fetch-all", views.hospital_medical_history_donors_viewset, name="hospital-fetch-donors"),
    path("hospital/<int:donor>/medical-history/fetch-all", views.hospital_donor_medical_history_viewset, name="hospital-fetch-donor-medical-history"),
    path("hospital/<int:donor>/<int:appointment>/medical-history/add", views.hospital_donor_medical_history_viewset, name="hospital-add-donor-medical-history"),
    path("hospital/<int:donor>/recent-appointments", views.donor_recent_appointments_viewset, name="hospital-fetch-donor-recent-donations"),
]
