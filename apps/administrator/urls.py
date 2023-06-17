from . import views
from django.urls import path

urlpatterns = [
    path('dashboard-info', views.dashboard_viewset, name="dashboard-info"),
    path('integrations/fetch-all', views.integrations_viewset, name="fetch-integrations"),
    path('integrations/approve/<int:organization>', views.integrations_viewset, name="patch-integration"),
    path('customers/hospitals/fetch-all', views.hospitals_viewset, name="fetch-hospitals"),
    path('customers/hospital/update/<int:hospital>', views.hospitals_viewset, name="update-hospital-info"),
    path('customers/donors/fetch-all', views.donors_viewset, name="fetch-donors"),
    path('customers/donor/update/<int:donor>', views.donors_viewset, name="update-donor-info"),
    path('customers/search/<str:query>', views.search_customers_viewset, name="search-customers"),
    path('donations/fetch-all', views.donations_viewset, name="fetch-donations"),
    path('complaints/fetch-all', views.complaints_viewset, name="fetch-complaints"),
    path('complaints/<int:complaint>/update-status', views.complaints_viewset, name="patch-complaint-status"),
    path('complaints/<int:complaint>/fetch-history', views.complaint_history_viewset, name="fetch-complaint-history"),
    path('complaints/<int:complaint>/reply-thread', views.complaint_history_viewset, name="reply-complaint-thread"),
    path('notifications/fetch-all', views.notifications_viewset, name="fetch-notifications"),
    path('notifications/create', views.notifications_viewset, name="create-notifications"),
    path('payment-history/add-record', views.paymenthistory_viewset, name="add-payment-history"),
]