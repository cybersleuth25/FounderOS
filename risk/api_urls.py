from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from risk.models import RiskReport
from founderos.ai_service import generate_risk_analysis
import json


class RiskAnalyzeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        startup_name = request.data.get('startup_name', '')
        industry = request.data.get('industry', '')
        stage = request.data.get('stage', '')
        description = request.data.get('description', '')
        if not startup_name:
            return Response({'error': 'startup_name is required'}, status=400)
        result = generate_risk_analysis(startup_name, industry, stage, description)
        return Response(result)


urlpatterns = [
    path('risk/analyze/', RiskAnalyzeAPI.as_view(), name='api_risk_analyze'),
]
