from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Report, ReportAttachment
from .forms import ReportForm, ReportAttachmentForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
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
        report = filledform.save()
        for file in request.FILES.getlist("attachment"):
            reportattachment = ReportAttachment()
            reportattachment.attachment = file
            reportattachment.report = report
            reportattachment.attachmenthash = get_hash(file)
            reportattachment.save()
        return HttpResponseRedirect('/reports/' + str(report.pk))
    mainform = ReportForm()
    fileform = ReportAttachmentForm()
    return render(request, 'reports/newreport.html', {'mainform': mainform, 'fileform': fileform})

@login_required()
def editreport(request, report_id):
    AttachmentFormSet = modelformset_factory(ReportAttachment, exclude=('report','attachmenthash'), extra=1)
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        formset = AttachmentFormSet(request.POST, request.FILES, queryset=report.reportattachment_set.all())
        instances = formset.save(commit=False)
        for reportattachment in instances:
            reportattachment.report = report
            if reportattachment.attachment:
                reportattachment.attachmenthash = get_hash(reportattachment.attachment)
                reportattachment.save()
            else:
                reportattachment.delete()
        return HttpResponseRedirect('/reports/' + str(report_id))
    mainform = ReportForm(instance=report)
    formset = AttachmentFormSet(queryset=report.reportattachment_set.all())
    return render(request, 'reports/editreport.html', {'mainform': mainform, 'formset': formset})
