from django.contrib import admin
from .models import FounderProfile


@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'startup_name', 'industry', 'stage', 'location', 'created_at']
    list_filter = ['industry', 'stage']
    search_fields = ['user__username', 'startup_name', 'location']
