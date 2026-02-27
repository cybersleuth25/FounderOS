from django.db import models
from django.contrib.auth.models import User


class RiskReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='risk_reports')
    startup_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    # Risk scores (0-100)
    financial_risk = models.IntegerField(null=True, blank=True)
    market_risk = models.IntegerField(null=True, blank=True)
    operational_risk = models.IntegerField(null=True, blank=True)
    overall_score = models.IntegerField(null=True, blank=True)
    # SWOT
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    opportunities = models.TextField(blank=True)
    threats = models.TextField(blank=True)
    # AI outputs
    mitigation_suggestions = models.TextField(blank=True)
    full_report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Risk Report — {self.startup_name} ({self.user.username})"
