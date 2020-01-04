from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from subscriptions import forms
from subscriptions.models import Subscriber
from tags.models import Tag
from status.models import Status
from report_admin.models import BasicReport


class SubscriptionsCreateView(LoginRequiredMixin, CreateView):
	"""docstring for Subscriptions"""
	template_name = 'subscriptions/subscription_settings.html'
	form_class = forms.SubscriptionForm
	success_url = reverse_lazy('subscriptions:subscriptions_create_view_success')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]

		return context


	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		SubscriptionForm = form.save(commit=False)
		SubscriptionForm.user = self.request.user
		SubscriptionForm = form.save()
		return super().form_valid(form)

class SubscriptionsCreateViewSuccess(LoginRequiredMixin, TemplateView):
	"""docstring for Subscriptions"""
	template_name = 'subscriptions/subscriptions_subscribed.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]

		try:
			subscriber = get_object_or_404(Subscriber,
								user=self.request.user)
			context['subscriber'] = subscriber
		except Exception:
			pass

		return context


class SubscriptionsUpdateView(LoginRequiredMixin, UpdateView):
	"""docstring for Subscriptions"""
	template_name = 'subscriptions/subscription_settings.html'
	form_class = forms.SubscriptionForm
	slug_field = 'subscriber_slug'
	slug_url_kwarg = 'subscriber_slug'
	success_url = reverse_lazy('subscriptions:subscriptions_update_view_success')

	def get_queryset(self):
		return Subscriber.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context

		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]
		
		try:
			subscriber = get_object_or_404(Subscriber,
								user=self.request.user)
			context['subscriber'] = subscriber
		except Exception:
			pass

		return context

class SubscriptionsUpdateViewSuccess(LoginRequiredMixin, TemplateView):
	"""docstring for Subscriptions"""
	template_name = 'subscriptions/subscriptions_updated.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]

		try:
			subscriber = get_object_or_404(Subscriber,
								user=self.request.user)
			context['subscriber'] = subscriber
		except Exception:
			pass

		return context


class SubscriptionsDeleteView(LoginRequiredMixin, DeleteView):
	model = Subscriber
	template_name = 'subscriptions/subscriptions_unsubscribed_confirm.html'
	slug_field = 'subscriber_slug'
	slug_url_kwarg = 'subscriber_slug'
	success_url = reverse_lazy('subscriptions:subscriptions_delete_view_success')

	def get_queryset(self):
		return Subscriber.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]

		try:
			subscriber = get_object_or_404(Subscriber,
								user=self.request.user)
			context['subscriber'] = subscriber
		except Exception:
			pass

		return context


class SubscriptionsDeleteViewSuccess(LoginRequiredMixin, TemplateView):
	template_name = 'subscriptions/subscriptions_unsubscribed.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		pulished_status = Status.objects.get(title="published")
		recent_reports = BasicReport.objects.filter(status=pulished_status).order_by('-id')[:10][::-1]
		tag_list = []
		for report in recent_reports:
			tag_list += report.tags.all()
		clean_tag_list = list(set(tag_list))
		context['recent_tags'] = clean_tag_list[::-1]

		try:
			subscriber = get_object_or_404(Subscriber,
								user=self.request.user)
			context['subscriber'] = subscriber
		except Exception:
			pass

		return context
