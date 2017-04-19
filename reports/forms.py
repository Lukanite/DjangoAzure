from django.forms import ModelForm
from reports.models import Report, ReportAttachment

class ReportForm(ModelForm):
    class Meta:
        model = Report
        exclude = ['release_date']

class ReportAttachmentForm(ModelForm):
    class Meta:
        model = ReportAttachment
        labels = {
            'attachment': ('Attachment(s)'),
        }
        exclude = ['report', 'attachmenthash']
