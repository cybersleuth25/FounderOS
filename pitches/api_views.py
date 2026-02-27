"""REST API endpoints for Pitch generation"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pitches.models import Pitch
from founderos.ai_service import generate_pitch_analysis
import json


class PitchGenerateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        if not title:
            return Response({'error': 'title is required'}, status=400)
        result = generate_pitch_analysis(title, description, description)
        return Response(result)


pitch_api_urls = [
    ('pitch/generate/', PitchGenerateAPI.as_view(), 'api_pitch_generate'),
]
