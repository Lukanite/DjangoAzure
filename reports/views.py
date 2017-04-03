from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Report
from .forms import ReportForm

# Create your views here.

def reportlist(request):
    reports = Report.objects.all()
    return render(request, 'reports/list.html', {'reports': reports})

def detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'reports/detail.html', {'report': report})

def newreport(request):
    if request.method == 'POST':
        filledform = ReportForm(request.POST)
        report = filledform.save()
        return render(request, 'reports/detail.html', {'report': report})
    form = ReportForm()
    return render(request, 'reports/newreport.html', {'form': form})

def editreport(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        filledform = ReportForm(request.POST, instance=report)
        filledform.save()
        return render(request, 'reports/detail.html', {'report': report})
    form = ReportForm(instance=report)
    return render(request, 'reports/newreport.html', {'form': form})
