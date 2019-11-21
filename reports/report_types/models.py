import datetime
import decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def current_year():
        return int(datetime.datetime.now().year)

def number():
    if BasicReport.objects.exists():
        last_year_entered = (
            BasicReport.objects.last().report_id_year
            )
        if current_year == last_year_entered:
            no = BasicReport.objects.filter(
                report_id_year=current_year
                ).select_for_update().aggregate(
                Max('report_id_number')
                )
            no = int(no['report_id_number__max'])+1
            no_string = str(no).zfill(9)
            return '{}'.format(no_string)
        else:
            return '1'.zfill(9)
    else:
        return '1'.zfill(9)


class BasicReportVersion(models.Model):
    version = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        )
    basic_report = models.ForeignKey(
        'BasicReport',
        on_delete=models.CASCADE,
        )
    basic_report_author_as_string = models.CharField(
        max_length=250,
        blank=True,
        )
    basic_report_reviewer_as_string = models.CharField(
        max_length=250,
        blank=True,
        )
    basic_report_title = models.CharField(
        max_length=250,
        blank=True,
        )
    basic_report_title_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        )
    basic_report_title_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        )
    basic_report_executive_summary = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_executive_summary_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_executive_summary_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_introduction = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_introduction_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_introduction_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_body = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_body_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_body_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_conclusion = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_conclusion_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_conclusion_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_recommendations = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_recommendations_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_recommendations_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_references = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_references_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_references_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        )
    basic_report_tags_as_string = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        )
    basic_report_tags_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_tags_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        ) 


    def basic_report_tags_as_string_as_list(self):
        return self.basic_report_tags_as_string.split(',')

    def save(self, *args, **kwargs):
        if (
            self.basic_report.status.title == 'sent_for_edit' or
            self.basic_report.status.title == 'typo_sent_for_edit'
            ):

            self.version = self.basic_report.version
            self.basic_report_reviewer_as_string = (
                self.basic_report.reviewer_as_string
                )

            self.basic_report_title = self.basic_report.title            
            self.basic_report_title_peer_review = (
                self.basic_report.title_peer_review
                )
            self.basic_report_title_peer_review_response = (
                self.basic_report.title_peer_review_response
                )

            self.basic_report_executive_summary = (
                self.basic_report.executive_summary
                )
            self.basic_report_executive_summary_peer_review = (
                self.basic_report.executive_summary_peer_review
                )
            self.basic_report_executive_summary_peer_review_response = (
                self.basic_report.executive_summary_peer_review_response
                )

            self.basic_report_introduction = self.basic_report.introduction            
            self.basic_report_introduction_peer_review = (
                self.basic_report.introduction_peer_review
                )
            self.basic_report_introduction_peer_review_response = (
                self.basic_report.introduction_peer_review_response
                )

            self.basic_report_body = self.basic_report.body            
            self.basic_report_body_peer_review = (
                self.basic_report.body_peer_review
                )
            self.basic_report_body_peer_review_response = (
                self.basic_report.body_peer_review_response
                )

            self.basic_report_conclusion = self.basic_report.conclusion            
            self.basic_report_conclusion_peer_review = (
                self.basic_report.conclusion_peer_review
                )
            self.basic_report_conclusion_peer_review_response = (
                self.basic_report.conclusion_peer_review_response
                )

            self.basic_report_recommendations = (
                self.basic_report.recommendations
                )
            self.basic_report_recommendations_peer_review = (
                self.basic_report.recommendations_peer_review
                )
            self.basic_report_recommendations_peer_review_response = (
                self.basic_report.recommendations_peer_review_response
                )

            self.basic_report_references = self.basic_report.references            
            self.basic_report_references_peer_review = (
                self.basic_report.references_peer_review
                )
            self.basic_report_references_peer_review_response = (
                self.basic_report.references_peer_review_response)

            self.basic_report_tags_as_string = (
                self.basic_report.tags_as_string
                )
            self.basic_report_tags_peer_review = (
                self.basic_report.tags_peer_review
                )
            self.basic_report_tags_peer_review_response = (
                self.basic_report.tags_peer_review_response
                )

        super(BasicReportVersion, self).save(*args, **kwargs)


class BasicReport(models.Model):
    """docstring for BasicReport"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="author",
        )
    author_as_string = models.CharField(
        max_length=300, 
        blank=True,
        )
    title = models.CharField(
        max_length=1000, 
        unique=True, 
        blank=True, 
        null=True
        )
    title_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    title_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    executive_summary = models.TextField(
        max_length=100000, 
        blank=True,
        )
    executive_summary_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    executive_summary_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        ) 
    introduction = models.TextField(
        max_length=100000, 
        blank=True,
        )
    introduction_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    introduction_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    body = models.TextField(
        max_length=100000, 
        blank=True,
        ) 
    body_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    body_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    conclusion = models.TextField(
        max_length=100000, 
        blank=True,
        )
    conclusion_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    conclusion_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        ) 
    recommendations = models.TextField(
        max_length=100000, 
        blank=True,
        )
    recommendations_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    recommendations_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    references = models.TextField(
        max_length=100000, 
        blank=True,
        ) 
    references_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        )
    references_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    tags_as_string = models.TextField(
        max_length=1000, 
        blank=True,
        )
    tags = models.ManyToManyField(
        Tag, 
        related_name='tags', 
        blank=True,
        )
    tags_peer_review = models.TextField(
        max_length=1000, 
        blank=True,
        )
    tags_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="reviewer",
        )
    reviewer_as_string = models.CharField(
        max_length=300, 
        blank=True, 
        )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT,
        related_name="status",
        )
    basic_report_id_number = models.CharField(
        default=number, 
        editable=False, 
        max_length=10
        )
    basic_report_id_year = models.PositiveIntegerField(
        default=current_year, 
        editable=False
        )
    version = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        editable=False,
        )
    update_comment = models.TextField(
        max_length=5000, 
        blank=True,
        )
    update = models.BooleanField(
        default=False, 
        blank=True,
        )
    typo_update = models.BooleanField(
        default=False, 
        blank=True,
        )
    date_created = models.DateTimeField(
        auto_now_add=True,
        )
    date_modified = models.DateTimeField(
        auto_now=True,
        )
    date_published = models.DateTimeField(
        null=True, 
        blank=True,
        )
    edited_in_admin_by = models.CharField(
        max_length=300, 
        blank=True,
        )


    def __init__(self, arg):
        super(BasicReport, self).__init__()
        self.arg = arg

    def __str__(self):
        return 'Report-{}-{}'.format(
            self.basic_report_id_year, 
            self.basic_report_id_number,
            )

    def summary_history(self):
        return BasicReportVersion.objects.filter(
            basic_report=self
            ).order_by('-version')

    def save(self, *args, **kwargs):
        if self.status.title == 'sent_for_review':
            self.title_peer_review = None
            self.executive_summary_peer_review = None
            self.introduction_peer_review = None
            self.body_peer_review = None
            self.conclusion_peer_review = None
            self.recommendations_peer_review = None
            self.references_peer_review = None
            self.tags_peer_review = None

        if self.status.title == 'sent_for_edit':
            self.title_peer_review_response = None
            self.executive_summary_peer_review_response = None
            self.introduction_peer_review_response = None
            self.body_peer_review_response = None
            self.conclusion_peer_review_response = None
            self.recommendations_peer_review_response = None
            self.references_peer_review_response = None
            self.tags_peer_review_response = None
                
        if self.status.title == 'published':
            self.title_peer_review = None
            self.title_peer_review_response = None
            self.executive_summary_peer_review = None
            self.executive_summary_peer_review_response = None
            self.introduction_peer_review = None
            self.introduction_peer_review_response = None
            self.body_peer_review = None
            self.body_peer_review_response = None
            self.conclusion_peer_review = None
            self.conclusion_peer_review_response = None
            self.recommendations_peer_review = None
            self.recommendations_peer_review_response = None
            self.references_peer_review = None
            self.references_peer_review_response = None
            self.tags_peer_review = None
            self.tags_peer_review_response = None

        current_version = self.version

        if self.status.title == 'first_draft':
            self.version = decimal.Decimal(.00)

        elif (
            self.status.title == 'sent_for_review' or
            self.status.title == 'typo_sent_for_review'
            ):
            self.version = current_version + decimal.Decimal(.01)

        elif self.status.title == 'published':
            if self.date_published:
                self.typo_update = False
                self.update = False
                self.update_comment = None

                if self.typo_update:
                    self.version = math.floor(current_version)
                else:
                    self.version = math.ceil(current_version)
            else:
                self.date_published = timezone.now()
                self.version = math.ceil(current_version)
      
        super(BasicReport, self).save(*args, **kwargs)

        if (
            self.status.title == "sent_for_edit" or
            self.status.title == "typo_sent_for_edit"
            ):
            newSummary = BasicReportVersion(basic_report=self)
            newSummary.save()
