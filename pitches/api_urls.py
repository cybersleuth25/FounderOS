from django.urls import path
from .api_views import PitchGenerateAPI

urlpatterns = [
    path('pitch/generate/', PitchGenerateAPI.as_view(), name='api_pitch_generate'),
]
