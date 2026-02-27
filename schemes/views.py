from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SchemeMatch, GovernmentScheme
from accounts.models import FounderProfile
from founderos.ai_service import generate_scheme_matches


@login_required
def schemes_home(request):
    profile, _ = FounderProfile.objects.get_or_create(user=request.user)
    matches = SchemeMatch.objects.filter(user=request.user)
    return render(request, 'schemes/schemes.html', {
        'matches': matches,
        'profile': profile,
    })


@login_required
def schemes_match(request):
    if request.method == 'POST':
        industry = request.POST.get('industry', '')
        stage = request.POST.get('stage', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')

        # Clear old matches for user
        SchemeMatch.objects.filter(user=request.user).delete()

        results = generate_scheme_matches(industry, stage, location, description)
        for r in results:
            SchemeMatch.objects.create(
                user=request.user,
                scheme_name=r.get('scheme_name', ''),
                eligibility_score=r.get('eligibility_score', 50),
                reasoning=r.get('reasoning', ''),
                status=r.get('status', 'partially'),
            )
        messages.success(request, f'Found {len(results)} scheme matches!')
    return redirect('schemes_home')
