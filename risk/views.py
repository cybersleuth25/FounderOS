from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RiskReport
from founderos.ai_service import generate_risk_analysis
import json


@login_required
def risk_home(request):
    reports = RiskReport.objects.filter(user=request.user)
    latest = reports.first()
    return render(request, 'risk/risk.html', {'reports': reports, 'latest': latest})


@login_required
def risk_analyze(request):
    if request.method == 'POST':
        startup_name = request.POST.get('startup_name', '').strip()
        industry = request.POST.get('industry', '').strip()
        stage = request.POST.get('stage', '').strip()
        description = request.POST.get('description', '').strip()

        if not startup_name or not description:
            messages.error(request, 'Startup name and description are required.')
            return redirect('risk_home')

        result = generate_risk_analysis(startup_name, industry, stage, description)

        report = RiskReport(
            user=request.user,
            startup_name=startup_name,
            industry=industry,
            stage=stage,
            description=description,
            financial_risk=result.get('financial_risk', 50),
            market_risk=result.get('market_risk', 50),
            operational_risk=result.get('operational_risk', 50),
            overall_score=result.get('overall_score', 50),
            strengths=json.dumps(result.get('strengths', [])),
            weaknesses=json.dumps(result.get('weaknesses', [])),
            opportunities=json.dumps(result.get('opportunities', [])),
            threats=json.dumps(result.get('threats', [])),
            mitigation_suggestions=json.dumps(result.get('mitigation_suggestions', [])),
            full_report=json.dumps(result),
        )
        report.save()
        messages.success(request, 'Risk analysis completed!')
        return redirect('risk_report', pk=report.pk)
    return redirect('risk_home')


@login_required
def risk_report(request, pk):
    from django.shortcuts import get_object_or_404
    report = get_object_or_404(RiskReport, pk=pk, user=request.user)

    def parse_json_field(field):
        try:
            return json.loads(field) if field else []
        except Exception:
            return []

    context = {
        'report': report,
        'strengths': parse_json_field(report.strengths),
        'weaknesses': parse_json_field(report.weaknesses),
        'opportunities': parse_json_field(report.opportunities),
        'threats': parse_json_field(report.threats),
        'mitigations': parse_json_field(report.mitigation_suggestions),
    }
    return render(request, 'risk/risk_report.html', context)
