from django.forms import ModelForm

from report_types.models import BasicReport

class BasicReportForm(ModelForm):
    class Meta:
        model = BasicReport
        fields = [
        	'reviewer',
        	'title',
        	'executive_summary',
        	'introduction',
        	'body',
        	'conclusion',
        	'recommendations',
        	'references',
        	'tags_as_string',
        	]
