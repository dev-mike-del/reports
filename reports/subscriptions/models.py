import itertools
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from tags.models import Tag


# The Subscriber class is used to create an subscriber. An Subscriber can
# subscrib to tags and receive email notifications.
class Subscriber(models.Model):
	'''Creates an Subscriber. A Subscriber is a Nike user who subscripbs to products.'''
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,
							related_name='subscriber_user',
							null=True,
							blank=True,
							)
	tags = models.ManyToManyField(Tag, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	created_by = models.CharField(max_length=100 ,null=True, blank=True)
	subscriber_slug = models.SlugField(
		unique=True, 
		default=uuid.uuid4, 
		max_length=255)

	def __str__(self):
		return '{}'.format(self.user.username,)

	def get_absolute_url(self):
		return 'subscriptions:subscriptions_update_view', (self.subscriber_slug,)

	def save(self, *args, **kwargs):
		max_length = Subscriber._meta.get_field('subscriber_slug').max_length
		self.subscriber_slug = orig = slugify(self)[:max_length]

		for x in itertools.count(1):
			if not Subscriber.objects.filter(subscriber_slug=self.subscriber_slug).exists():
				break
			if Subscriber.objects.filter(subscriber_slug=self.subscriber_slug, id=self.id).exists():
				break
			self.subscriber_slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)


		super(Subscriber, self).save(*args, **kwargs)
