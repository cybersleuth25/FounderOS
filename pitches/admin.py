from django.contrib import admin
from .models import Pitch


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'overall_score', 'clarity_score', 'engagement_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'user__username']
