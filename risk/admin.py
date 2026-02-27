from django.contrib import admin
from .models import RiskReport


@admin.register(RiskReport)
class RiskReportAdmin(admin.ModelAdmin):
    list_display = ['startup_name', 'user', 'overall_score', 'financial_risk', 'market_risk', 'operational_risk', 'created_at']
    list_filter = ['industry', 'stage']
    search_fields = ['startup_name', 'user__username']
