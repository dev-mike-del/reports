from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class BasicReport(models.Model):
	"""docstring for BasicReport"""
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET(get_sentinel_user),
		related_name="author",
		)
	title = models.CharField(max_length=500)
	executive_summary = models.TextField(blank=True) 
	introduction = models.TextField(blank=True)
	body = models.TextField(blank=True) 
	conclusion = models.TextField(blank=True) 
	recommendations = models.TextField(blank=True)
	references = models.TextField(blank=True) 
	reviewer = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET(get_sentinel_user),
		related_name="reviewer",
		)


	def __init__(self, arg):
		super(BasicReport, self).__init__()
		self.arg = arg


		
