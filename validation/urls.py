from django.urls import path
from . import views

urlpatterns = [
    path('', views.validation_home, name='validation_home'),
    path('upload/', views.upload_document, name='validation_upload'),
    path('delete/<int:pk>/', views.delete_document, name='validation_delete'),
]
