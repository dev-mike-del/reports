from django.forms import ModelForm

from report_admin.models import BasicReport

class BasicReportForm(ModelForm):
    class Meta:
        model = BasicReport
        fields = [
        	'title',
        	'executive_summary',
        	'introduction',
        	'body',
        	'conclusion',
        	'recommendations',
        	'references',
        	'tags_as_string',
        	'reviewer',]