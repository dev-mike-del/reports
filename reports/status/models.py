from django.db import models


class Status(models.Model):
    '''Creates a Status Title and Description.
    This is used to identify the workflow position of the Threat report'''
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
