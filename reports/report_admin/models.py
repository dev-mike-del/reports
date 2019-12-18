import datetime
import decimal
import itertools
import math
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from status.models import Status
from tags.models import Tag


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def current_year():
        return int(datetime.datetime.now().year)

def number():
        if BasicReport.objects.exists():
            current_year = int(datetime.datetime.now().year)
            last_year_entered = (BasicReport.objects.last()
                                .basic_report_id_year)
            if current_year == last_year_entered:
                no = BasicReport.objects.filter(version >= 1).select_for_update().aggregate(
                    models.Max('id_number'))
                no = int(no['id_number__max'])+1
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
        null=True
        )
    basic_report_title_peer_review = models.TextField(
        max_length=1000,
        blank=True,
        null=True
        )
    basic_report_title_peer_review_response = models.TextField(
        max_length=1000,
        blank=True,
        null=True
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
    basic_report_unique_id = models.UUIDField(
        editable=False, 
        unique=False
        ) 
    date = models.DateTimeField(auto_now_add=True)


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
            self.basic_report_unique_id = (
                self.basic_report.unique_id
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
        null=True
        )
    title_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    executive_summary = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    executive_summary_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    executive_summary_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        ) 
    introduction = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    introduction_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    introduction_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    body = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        ) 
    body_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    body_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    conclusion = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    conclusion_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    conclusion_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        ) 
    recommendations = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    recommendations_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    recommendations_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    references = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        ) 
    references_peer_review = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    references_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
        )
    tags_as_string = models.TextField(
        max_length=1000, 
        blank=True,
        null=True
        )
    tags = models.ManyToManyField(
        Tag, 
        related_name='tags', 
        blank=True,
        )
    tags_peer_review = models.TextField(
        max_length=1000, 
        blank=True,
        null=True
        )
    tags_peer_review_response = models.TextField(
        max_length=100000, 
        blank=True,
        null=True
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
    id_number = models.CharField(
        null=True,
        editable=True, 
        max_length=10
        )
    id_year = models.PositiveIntegerField(
        null=True,
        editable=True
        )
    version = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        editable=False,
        null=True
        )
    update_comment = models.TextField(
        max_length=5000, 
        blank=True,
        null=True
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
    slug = models.SlugField(
        unique=True, 
        default=uuid.uuid4, 
        max_length=255
        )
    unique_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
        )

    def __str__(self):
        if (self.status.title == "published" or
            self.version >= 1):
            return 'Report-{}-{}'.format(
                self.id_year, 
                self.id_number,
                )
        else:
            return 'Report-{}'.format(self.slug)

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

        current_version = self.version

        if (
            self.status.title == 'sent_for_review' or
            self.status.title == 'typo_sent_for_review'
            ):
            if not current_version:
                current_version = decimal.Decimal(.00)

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

            if self.version == 1:
                max_length = BasicReport._meta.get_field('slug').max_length
                self.slug = orig = slugify(self)[:max_length]

                for x in itertools.count(1):
                    if not BasicReport.objects.filter(slug=self.slug).exists():
                        break
                    if BasicReport.objects.filter(slug=self.slug, id=self.id).exists():
                        break
                    self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
      
        super(BasicReport, self).save(*args, **kwargs)

        if (
            self.status.title == "sent_for_edit" or
            self.status.title == "typo_sent_for_edit"
            ):
            newSummary = BasicReportVersion(basic_report=self)
            newSummary.save()
