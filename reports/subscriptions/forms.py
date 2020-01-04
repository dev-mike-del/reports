from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.encoding import smart_text

from subscriptions.models import Subscriber
from tags.models import Tag

User = get_user_model()

def get_tags(self):
	subscriber = Subscriber.objects.get(user=self.request.user)
	subscriber_tags = subscriber.tags
	return subscriber_tags.filter(title__range=('A','E')).order_by('title')



class SubscriptionForm(forms.ModelForm):
	tags = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple,
		required=False,
		queryset=Tag.objects.all().order_by('title'),)

	class Meta:
		model = Subscriber
		fields = ['tags',]