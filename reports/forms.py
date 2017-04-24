from django.forms import ModelForm
from reports.models import Report, ReportAttachment
from django.forms import ModelChoiceField
from django.contrib.auth.models import Group

class ReportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        if (user.profile.user_type == 'site_manager'):
            self.fields['group'] = ModelChoiceField(
                queryset=Group.objects.all()
            )
        else:
            self.fields['group'] = ModelChoiceField(
                queryset=user.groups.filter()
            )

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
