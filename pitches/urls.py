from django.urls import path
from . import views
from .gallery_views import pitch_gallery

urlpatterns = [
    path('', views.pitch_lab, name='pitch_lab'),
    path('create/', views.pitch_create, name='pitch_create'),
    path('gallery/', pitch_gallery, name='pitch_gallery'),
    path('<int:pk>/', views.pitch_detail, name='pitch_detail'),
    path('<int:pk>/delete/', views.pitch_delete, name='pitch_delete'),
]
