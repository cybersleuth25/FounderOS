from django.urls import path
from . import views

urlpatterns = [
    path('', views.schemes_home, name='schemes_home'),
    path('match/', views.schemes_match, name='schemes_match'),
]
