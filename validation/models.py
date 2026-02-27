from django.db import models
from django.contrib.auth.models import User


VALIDATION_STATUS = [
    ('pending', 'Pending'),
    ('pass', 'Passed'),
    ('fail', 'Failed'),
    ('review', 'Under Review'),
]


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=300)
    file = models.FileField(upload_to='documents/')
    ocr_text = models.TextField(blank=True)
    validation_status = models.CharField(max_length=10, choices=VALIDATION_STATUS, default='pending')
    report = models.TextField(blank=True)
    issues_found = models.IntegerField(default=0)
    suggestions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.validation_status}"
