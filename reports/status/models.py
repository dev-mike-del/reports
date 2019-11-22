from django.db import models


class Status(models.Model):
    '''Creates a Status Title and Description.
    This is used to identify the workflow position of the Threat report'''
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, title):
        status = cls(title=title)
        # do something with the status
        return status


### Threat Statuses ###
try:
    first_draft = Status.objects.get(title="first_draft")
except Exception as e:
    pass
else:
    first_draft = Status.create(title="first_draft")
    author_draft = Status.create(title="author_draft")
    sent_for_review = Status.create(title="sent_for_review")
    sent_for_edit = Status.create(title="sent_for_edit")
    edit_draft = Status.create(title="edit_draft")
    in_edit = Status.create(title="in_edit")
    in_review = Status.create(title="in_review")
    review_draft = Status.create(title="review_draft")
    published = Status.create(title="published")
    archived = Status.create(title="archived")
