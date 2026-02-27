from django.contrib import admin
from .models import MatchProfile, MatchRequest


@admin.register(MatchProfile)
class MatchProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'industry', 'location', 'is_available']
    list_filter = ['role', 'is_available']
    search_fields = ['name', 'industry', 'skills']


@admin.register(MatchRequest)
class MatchRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile', 'created_at']
