from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('mentor', 'Mentor'),
    ('cofounder', 'Co-founder'),
    ('investor', 'Investor'),
    ('advisor', 'Advisor'),
]


class MatchProfile(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    location = models.CharField(max_length=200, blank=True)
    contact = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class MatchRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_requests')
    profile = models.ForeignKey(MatchProfile, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.profile.name}"
