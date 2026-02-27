from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MatchProfile, MatchRequest
from accounts.models import FounderProfile


@login_required
def matching_home(request):
    profile, _ = FounderProfile.objects.get_or_create(user=request.user)
    role_filter = request.GET.get('role', '')
    profiles = MatchProfile.objects.filter(is_available=True)
    if role_filter:
        profiles = profiles.filter(role=role_filter)
    # Filter by industry if profile has one
    if profile.industry and not role_filter:
        industry_matches = profiles.filter(industry__icontains=profile.industry)
        other_matches = profiles.exclude(industry__icontains=profile.industry)
        profiles = list(industry_matches) + list(other_matches)
    my_requests = MatchRequest.objects.filter(user=request.user)
    return render(request, 'matching/matching.html', {
        'profiles': profiles,
        'my_requests': my_requests,
        'role_filter': role_filter,
    })


@login_required
def send_match_request(request, pk):
    from .models import MatchProfile
    from django.shortcuts import get_object_or_404
    profile_obj = get_object_or_404(MatchProfile, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if not MatchRequest.objects.filter(user=request.user, profile=profile_obj).exists():
            MatchRequest.objects.create(
                user=request.user,
                profile=profile_obj,
                message=message,
            )
            messages.success(request, f'Connection request sent to {profile_obj.name}!')
        else:
            messages.info(request, 'You already sent a request to this person.')
    return redirect('matching_home')
