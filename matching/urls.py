from django.urls import path
from . import views

urlpatterns = [
    path('', views.matching_home, name='matching_home'),
    path('connect/<int:pk>/', views.send_match_request, name='match_connect'),
]
