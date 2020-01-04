from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse

from accounts.forms import CustomUserCreationForm
from report_admin.models import BasicReport
from users.models import User

from subscriptions.models import Subscriber


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("list")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.save()
        user = User.objects.get(username=form.username)
        login(self.request, user)
        return HttpResponseRedirect(reverse('accounts:profile'))


class ProflieListView(LoginRequiredMixin, ListView):
    """docstring for ProflieListView"""
    model = BasicReport
    template_name = "accounts/profile_list.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['reports_to_review'] = self.model.objects.filter(
                                    Q(reviewer=self.request.user),
                                    Q(status__title="sent_for_review")).all().order_by('-date_modified')

        context['reports_in_review'] = self.model.objects.filter(
                                    Q(reviewer=self.request.user),
                                    Q(status__title="review")).all().order_by('-date_modified')

        context['reports_sent_for_edit'] = self.model.objects.filter(
                                    Q(reviewer=self.request.user),
                                    Q(status__title="sent_for_edit") |
                                    Q(status__title="edit"),
                                    Q(version__gte=0)).all().order_by('-date_modified')

        
        context['reports_to_edit'] = self.model.objects.filter(
                                    Q(author=self.request.user),
                                    Q(status__title="sent_for_edit")).all().order_by('-date_modified')

    
        context['reports_in_edit'] = self.model.objects.filter(
                                    Q(author=self.request.user),
                                    Q(status__title="edit"),
                                    Q(version__gte=0)).all().order_by('-date_modified')

        
        context['new_reports_in_edit'] = self.model.objects.filter(
                                    Q(author=self.request.user),
                                    Q(status__title="edit"),
                                    Q(version=None)).all().order_by('-date_modified')

        
        context['reports_sent_for_review'] = self.model.objects.filter(
                                    Q(author=self.request.user),
                                    Q(status__title="sent_for_review") |
                                    Q(status__title="review")).all().order_by('-date_modified')

        try:
            user = User.objects.get(id=self.request.user.id)
            subscriber = Subscriber.objects.get(user=user)
            context['subscriber'] = subscriber
        except Exception:
            pass

        return context