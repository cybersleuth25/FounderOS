from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import FounderProfile
from pitches.models import Pitch
from risk.models import RiskReport
from schemes.models import SchemeMatch


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        startup_name = request.POST.get('startup_name', '').strip()
        industry = request.POST.get('industry', 'tech')
        location = request.POST.get('location', '').strip()

        if not username or not email or not password:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'accounts/signup.html')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        FounderProfile.objects.create(
            user=user,
            startup_name=startup_name,
            industry=industry,
            location=location,
        )
        login(request, user)
        messages.success(request, f'Welcome to FounderOS, {username}! 🚀')
        return redirect('dashboard')
    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def dashboard(request):
    from founderos.news_service import fetch_startup_news
    profile, _ = FounderProfile.objects.get_or_create(user=request.user)
    pitches = Pitch.objects.filter(user=request.user)[:5]
    latest_risk = RiskReport.objects.filter(user=request.user).first()
    scheme_matches = SchemeMatch.objects.filter(user=request.user)[:3]
    avg_score = pitches.aggregate(avg=Avg('overall_score'))['avg'] or 0
    news = fetch_startup_news(limit=5)
    context = {
        'profile': profile,
        'pitches': pitches,
        'latest_risk': latest_risk,
        'scheme_matches': scheme_matches,
        'pitch_count': pitches.count(),
        'avg_pitch_score': int(avg_score),
        'news': news,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = FounderProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.startup_name = request.POST.get('startup_name', '')
        profile.stage = request.POST.get('stage', 'idea')
        profile.industry = request.POST.get('industry', 'tech')
        profile.location = request.POST.get('location', '')
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        profile.linkedin = request.POST.get('linkedin', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'profile': profile})
