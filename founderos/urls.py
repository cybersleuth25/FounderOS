"""FounderOS URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('pitches/', include('pitches.urls')),
    path('risk/', include('risk.urls')),
    path('schemes/', include('schemes.urls')),
    path('matching/', include('matching.urls')),
    path('validation/', include('validation.urls')),
    # API endpoints
    path('api/', include('pitches.api_urls')),
    path('api/', include('risk.api_urls')),
    path('api/', include('schemes.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
