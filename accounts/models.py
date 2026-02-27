from django.db import models
from django.contrib.auth.models import User


STAGE_CHOICES = [
    ('idea', 'Idea Stage'),
    ('mvp', 'MVP Stage'),
    ('early', 'Early Traction'),
    ('growth', 'Growth Stage'),
]

INDUSTRY_CHOICES = [
    ('tech', 'Technology'),
    ('agri', 'Agriculture'),
    ('health', 'Healthcare'),
    ('edu', 'Education'),
    ('finance', 'FinTech'),
    ('retail', 'Retail/E-commerce'),
    ('logistics', 'Logistics'),
    ('other', 'Other'),
]


class FounderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='founder_profile')
    startup_name = models.CharField(max_length=200, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='idea')
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, default='tech')
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.startup_name or 'No Startup'}"
