from django.forms import ModelForm
from reports.models import Report

class ReportForm(ModelForm):
    class Meta:
            model = Report
            exclude = ['release_date', 'attachmenthash']
            