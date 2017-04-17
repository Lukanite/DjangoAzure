from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Report
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
import hashlib

def get_hash(file):
    md5 = hashlib.md5()
    for c in file.chunks():
        md5.update(c)
    return md5.hexdigest()

# Create your views here.

@login_required()
def reportlist(request):
    reports = Report.objects.all()
    return render(request, 'reports/list.html', {'reports': reports})

@login_required()

def detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'reports/detail.html', {'report': report})

@login_required()
def newreport(request):
    if request.method == 'POST':
        filledform = ReportForm(request.POST, request.FILES)
        report = filledform.save(commit=False)
        if report.attachment != None:
            report.attachmenthash = get_hash(report.attachment)
        report.save()
        return HttpResponseRedirect('/reports/' + str(report.pk))
    form = ReportForm()
    return render(request, 'reports/newreport.html', {'form': form})

@login_required()
def editreport(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        filledform = ReportForm(request.POST, request.FILES, instance=report)
        report = filledform.save(commit=False)
        if report.attachment != None:
            report.attachmenthash = get_hash(report.attachment)
        report.save()
        return HttpResponseRedirect('/reports/' + str(report_id))
    form = ReportForm(instance=report)
    return render(request, 'reports/newreport.html', {'form': form})
