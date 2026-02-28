from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from founderos.utils import ratelimit
from .models import Pitch
from founderos.ai_service import generate_pitch_analysis
import os
import json


@login_required
def pitch_lab(request):
    pitches = Pitch.objects.filter(user=request.user)
    return render(request, 'pitches/pitch_lab.html', {'pitches': pitches})


@login_required
@ratelimit(key='user', rate='10/h', block=True)
def pitch_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('pitch_lab')

        pitch = Pitch(user=request.user, title=title, description=description)
        
        ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.jpg', '.png']
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                messages.error(request, f'Unsupported file type: {ext}. Allowed: PDF, Word, Image.')
                return redirect('pitch_lab')
            pitch.file = uploaded_file
            
        if 'video' in request.FILES:
            pitch.video = request.FILES['video']
            
        pitch.save()

        # Generate AI analysis
        result = generate_pitch_analysis(title, description, description)
        pitch.clarity_score = result.get('clarity_score', 70)
        pitch.engagement_score = result.get('engagement_score', 70)
        pitch.overall_score = result.get('overall_score', 70)
        pitch.ai_report = json.dumps(result)
        pitch.save()

        messages.success(request, f'Pitch "{title}" analyzed successfully!')
        return redirect('pitch_detail', pk=pitch.pk)
    return redirect('pitch_lab')


@login_required
def pitch_detail(request, pk):
    pitch = get_object_or_404(Pitch, pk=pk, user=request.user)
    report = {}
    if pitch.ai_report:
        try:
            report = json.loads(pitch.ai_report)
        except Exception:
            pass
    return render(request, 'pitches/pitch_detail.html', {'pitch': pitch, 'report': report})


@login_required
def pitch_delete(request, pk):
    pitch = get_object_or_404(Pitch, pk=pk, user=request.user)
    if request.method == 'POST':
        pitch.delete()
        messages.success(request, 'Pitch deleted.')
    return redirect('pitch_lab')
