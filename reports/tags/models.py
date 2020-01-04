from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100 ,blank=True,
        null=True)
    modified_by = models.CharField(max_length=100 ,blank=True,
        null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()

        super(Tag, self).save(*args, **kwargs)