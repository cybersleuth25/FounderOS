from django.db import models
from django.contrib.auth.models import User


class Pitch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pitches')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='pitches/', null=True, blank=True)
    video = models.FileField(upload_to='pitch_videos/', null=True, blank=True)
    extracted_text = models.TextField(blank=True)
    ai_report = models.TextField(blank=True)
    clarity_score = models.IntegerField(null=True, blank=True)
    engagement_score = models.IntegerField(null=True, blank=True)
    overall_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.user.username}"
