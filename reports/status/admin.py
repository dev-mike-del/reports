from django.contrib import admin

from status.models import Status

### Threat Statuses ###
first_draft = Status.objects.get_or_create(title="first_draft")
author_draft = Status.objects.get_or_create(title="author_draft")
sent_for_review = Status.objects.get_or_create(title="sent_for_review")
sent_for_edit = Status.objects.get_or_create(title="sent_for_edit")
edit_draft = Status.objects.get_or_create(title="edit_draft")
in_edit = Status.objects.get_or_create(title="in_edit")
in_review = Status.objects.get_or_create(title="in_review")
review_draft = Status.objects.get_or_create(title="review_draft")
published = Status.objects.get_or_create(title="published")
archived = Status.objects.get_or_create(title="archived")


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


admin.site.register(Status, StatusAdmin)
