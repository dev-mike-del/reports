from django.forms import ModelForm

from report_admin.models import BasicReport

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

class BasicReportCommentForm(ModelForm):
    class Meta:
        model = BasicReport
        fields = [
            'title_peer_review',
            'executive_summary_peer_review',
            'introduction_peer_review',
            'body_peer_review',
            'conclusion_peer_review',
            'recommendations_peer_review',
            'references_peer_review',
            'tags_peer_review',
            ]
