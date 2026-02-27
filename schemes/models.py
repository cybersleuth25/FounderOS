from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('eligible', 'Eligible'),
    ('partially', 'Partially Eligible'),
    ('not_eligible', 'Not Eligible'),
    ('applied', 'Applied'),
    ('tracking', 'Tracking'),
]


class GovernmentScheme(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    ministry = models.CharField(max_length=200, blank=True)
    target_stage = models.CharField(max_length=100, blank=True)
    target_industry = models.CharField(max_length=200, blank=True)
    max_funding = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SchemeMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheme_matches')
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, null=True, blank=True)
    scheme_name = models.CharField(max_length=300)
    eligibility_score = models.IntegerField(null=True, blank=True)
    reasoning = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='eligible')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-eligibility_score']

    def __str__(self):
        return f"{self.scheme_name} — {self.user.username}"
