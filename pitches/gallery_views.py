"""
Public Pitch Gallery view — shows all pitches visible to logged-in users.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Pitch


@login_required
def pitch_gallery(request):
    """Public pitch gallery feed — all users' pitches visible to authenticated users."""
    search = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', '')  # 'video', 'text', 'all'

    pitches = Pitch.objects.select_related('user', 'user__founder_profile').order_by('-created_at')

    if search:
        pitches = pitches.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if filter_type == 'video':
        pitches = pitches.exclude(video='')
    elif filter_type == 'text':
        pitches = pitches.filter(video='')

    return render(request, 'pitches/gallery.html', {
        'pitches': pitches,
        'search': search,
        'filter_type': filter_type,
        'total_count': Pitch.objects.count(),
    })
