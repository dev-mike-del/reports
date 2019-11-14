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
    executive_summary = models.TextField(
        max_length=100000, 
        blank=True,
        )
    executive_summary_peer_review = models.TextField(
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
    body = models.TextField(
        max_length=100000, 
        blank=True,
        ) 
    body_peer_review = models.TextField(
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
    recommendations = models.TextField(
        max_length=100000, 
        blank=True,
        )
    recommendations_peer_review = models.TextField(
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
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="reviewer",
        )
    reviewer_as_string = models.CharField(
        max_length=300, 
        blank=True, 
        )
    report_id_number = models.CharField(
        default=number, 
        editable=False, 
        max_length=10
        )
    report_id_year = models.PositiveIntegerField(
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


        
