from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('api/news/', views.news_api, name='news_api'),
    path('api/aria/', views.aria_chat, name='aria_chat'),
]
