"""medexer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path('medexer/api/v1/', include('apps.user.urls')),
        path('medexer/api/v1/administrator/', include('apps.administrator.urls')),
        path('medexer/api/v1/registration/', include('apps.registration.urls')),
        path('medexer/api/v1/profile/', include('apps.profile.urls')),
        path('medexer/api/v1/donor/', include('apps.donor.urls')),
        path('medexer/api/v1/hospital/', include('apps.hospital.urls')),
        path('medexer/api/v1/auth/refresh-token', jwt_views.TokenRefreshView.as_view(), name="jwt_refresh"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
