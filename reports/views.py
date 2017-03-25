from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Report

# Create your views here.
def detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'reports/detail.html', {'report': report})
