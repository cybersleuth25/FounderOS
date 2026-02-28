from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from founderos.utils import ratelimit
from .models import Document


@login_required
def validation_home(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'validation/validation.html', {'documents': documents})


@login_required
@ratelimit(key='user', rate='15/h', block=True)
def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title or 'file' not in request.FILES:
            messages.error(request, 'Please provide a title and file.')
            return redirect('validation_home')

        doc = Document(
            user=request.user,
            title=title,
            file=request.FILES['file'],
        )
        doc.save()

        # Simple validation logic (no OCR in MVP, just file checks)
        filename = doc.file.name.lower()
        issues = []
        suggestions = []

        if not any(filename.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.jpg', '.png']):
            issues.append('Unsupported file format detected')
            suggestions.append('Upload PDF, Word, or image files for best results')

        file_size = doc.file.size
        if file_size < 1024:  # < 1KB
            issues.append('File appears to be empty or too small')
            suggestions.append('Ensure the document contains actual content')
        elif file_size > 10 * 1024 * 1024:  # > 10MB
            issues.append('File size exceeds recommended limit (10MB)')
            suggestions.append('Compress the file or split into smaller documents')

        doc.issues_found = len(issues)
        doc.validation_status = 'fail' if len(issues) > 0 else 'pass'
        doc.report = '\n'.join(issues) if issues else 'Document passed all basic validation checks.'
        doc.suggestions = '\n'.join(suggestions) if suggestions else 'No suggestions — document looks good!'
        doc.save()

        status = 'passed ✓' if doc.validation_status == 'pass' else 'flagged issues'
        messages.success(request, f'Document "{title}" validated — {status}')
        return redirect('validation_home')
    return redirect('validation_home')


@login_required
def delete_document(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, 'Document deleted.')
    return redirect('validation_home')
