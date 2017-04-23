from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Report, ReportAttachment
from .forms import ReportForm, ReportAttachmentForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
import hashlib

def get_hash(file):
    md5 = hashlib.md5()
    for c in file.chunks():
        md5.update(c)
    return md5.hexdigest()

def not_investor_user(user):
    return not user.profile.user_type == "investor_user"
# Create your views here.

@login_required()
def reportlist(request):
    all_reports = Report.objects.all()
    reports = []
    if request.user.profile.user_type == "site_manager":
        reports = all_reports
    else:
        user_groups = request.user.groups.filter()
        for r in all_reports:
            if r.isprivate:
                for g in user_groups:
                    if g.name == r.group.name:
                        reports.append(r)
            else:
                reports.append(r)
    return render(request, 'reports/list.html', {'reports': reports})

@login_required()
@csrf_exempt
def detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if (request.POST.get('delete')):
        deleted_report = Report.objects.get(id=report_id)
        deleted_report.delete()
        return HttpResponseRedirect('/reports')
    return render(request, 'reports/detail.html', {'report': report})

@login_required()
@user_passes_test(not_investor_user, login_url='/', redirect_field_name="")
def newreport(request):
    if request.method == 'POST':
        filledform = ReportForm(request.POST, user=request.user)
        report = filledform.save()
        for file in request.FILES.getlist("attachment"):
            reportattachment = ReportAttachment()
            reportattachment.attachment = file
            reportattachment.report = report
            reportattachment.attachmenthash = get_hash(file)
            reportattachment.save()
        return HttpResponseRedirect('/reports/' + str(report.pk))
    mainform = ReportForm(user=request.user)
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
    mainform = ReportForm(user=request.user, instance=report)
    formset = AttachmentFormSet(queryset=report.reportattachment_set.all())
    return render(request, 'reports/editreport.html', {'mainform': mainform, 'formset': formset, 'report': report})
