from django.forms import ModelForm

from report_admin.models import BasicReport

class BasicReportForm(ModelForm):
    class Meta:
        model = BasicReport
        fields = [
        	'title',
            'title_peer_review',
        	'executive_summary',
            'executive_summary_peer_review',
        	'introduction',
            'introduction_peer_review',
        	'body',
            'body_peer_review',
        	'conclusion',
            'conclusion_peer_review',
        	'recommendations',
            'recommendations_peer_review',
        	'references',
            'references_peer_review',
        	'tags_as_string',
            'tags_peer_review',
        	'reviewer',]
