from django.urls import path
from . import views

urlpatterns = [
    path('', views.risk_home, name='risk_home'),
    path('analyze/', views.risk_analyze, name='risk_analyze'),
    path('report/<int:pk>/', views.risk_report, name='risk_report'),
]
