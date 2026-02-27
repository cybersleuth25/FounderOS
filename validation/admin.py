from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'validation_status', 'issues_found', 'created_at']
    list_filter = ['validation_status']
    search_fields = ['title', 'user__username']
