from django import forms
from django.contrib.auth import get_user_model

from report_admin.models import BasicReport

from ckeditor.widgets import CKEditorWidget

class BasicReportForm(forms.ModelForm):
    reviewer = forms.ModelChoiceField(
                                queryset=get_user_model().objects.all(),
                                # empty_label="Unassigned | First Available",
                                empty_label="Choose",
                                widget=forms.Select(
                                          attrs={
                                            "class": "form-control",
                                            "id": "exampleFormControlSelect1",
                                                 }
                                               ),
                                required=False,)


    title = forms.CharField(max_length=250,
                            empty_value="Example of a Title",
                            widget=forms.TextInput(
                                       attrs={
                                        "type": "text",
                                        "class": "form-control",
                                        "id": "TitleTextArea",
                                        "maxlength": 60,
                                        "placeholder": "E.g. 'Cybercriminals Perform Attacks Against S3 Buckets'"},
                                           ),
                            required=False,)

    title_peer_review = forms.CharField(max_length=250,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "titleCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    executive_summary = forms.CharField(max_length=4000,
                                   widget=CKEditorWidget(
                                   attrs={
                                    "class": "form-control",
                                    "id": "executiveTextArea",
                                    "name": "executiveTextArea",
                                    "maxlength": 200,
                                    "rows": 5,},
                                          ),
                                   required=False,)

    executive_summary_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "executive_summaryCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    introduction = forms.CharField(max_length=4000,
                                   widget=CKEditorWidget(
                                   attrs={
                                    "class": "form-control",
                                    "id": "introductionTextArea",
                                    "name": "introductionTextArea",
                                    "maxlength": 600,
                                    "rows": 6,},
                                          ),
                                   required=False,)

    introduction_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "introductionCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    body = forms.CharField(max_length=4000,
                               widget=CKEditorWidget(
                               attrs={
                                "class": "form-control",
                                "id": "bodyTextArea",
                                "name": "bodyTextArea",
                                "maxlength": 600,
                                "rows": 6,},
                                      ),
                               required=False,)

    body_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "bodyCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    conclusion = forms.CharField(max_length=4000,
                                   widget=CKEditorWidget(
                                           attrs={
                                            "class": "form-control",
                                            "id": "conclusionTextArea",
                                            "name": "conclusionTextArea",
                                            "maxlength": 600,
                                            "rows": 6,},
                                                  ),
                                   required=False,)

    conclusion_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "conclusionCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    recommendations = forms.CharField(max_length=4000,
                                   widget=CKEditorWidget(
                                           attrs={
                                            "class": "form-control",
                                            "id": "recommendationsTextArea",
                                            "name": "recommendationsTextArea",
                                            "maxlength": 600,
                                            "rows": 6,},
                                                  ),
                                   required=False,)

    recommendations_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "recommendationsCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    references = forms.CharField(max_length=4000,
                                   widget=CKEditorWidget(
                                           attrs={
                                            "class": "form-control",
                                            "id": "referencesTextArea",
                                            "name": "referencesTextArea",
                                            "maxlength": 600,
                                            "rows": 6,},
                                                  ),
                                   required=False,)

    references_peer_review = forms.CharField(max_length=800,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "referencesCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)



    tags_as_string = forms.CharField(max_length=250,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "tags",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)

    tags_peer_review = forms.CharField(max_length=250,
                                   widget=forms.Textarea(
                                       attrs={
                                        "class": "form-control",
                                        "id": "tagsCommentsControlTextarea1",
                                        "placeholder": "Suggest a change here",
                                        "rows": 5,},
                                                  ),
                                   required=False,)
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
            'title_peer_review',
            'executive_summary_peer_review',
            'introduction_peer_review',
            'body_peer_review',
            'conclusion_peer_review',
            'recommendations_peer_review',
            'references_peer_review',
            'tags_peer_review',
        	]
    def __init__(self, *args, **kwargs):
        user = kwargs['initial'].pop('user', None)
        super(BasicReportForm, self).__init__(*args, **kwargs)
        self.fields['reviewer'].queryset = get_user_model().objects.all(
          ).order_by('last_name').exclude(id=user.id)



class BasicReportCommentForm(forms.ModelForm):
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
