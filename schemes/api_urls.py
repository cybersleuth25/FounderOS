from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from founderos.ai_service import generate_scheme_matches


class SchemeMatchAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        industry = request.data.get('industry', '')
        stage = request.data.get('stage', '')
        location = request.data.get('location', '')
        description = request.data.get('description', '')
        result = generate_scheme_matches(industry, stage, location, description)
        return Response(result)


urlpatterns = [
    path('schemes/match/', SchemeMatchAPI.as_view(), name='api_schemes_match'),
]
