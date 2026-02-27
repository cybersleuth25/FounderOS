from django.contrib import admin
from .models import GovernmentScheme, SchemeMatch


@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'max_funding', 'target_stage', 'is_active']
    list_filter = ['is_active']


@admin.register(SchemeMatch)
class SchemeMatchAdmin(admin.ModelAdmin):
    list_display = ['scheme_name', 'user', 'eligibility_score', 'status', 'created_at']
