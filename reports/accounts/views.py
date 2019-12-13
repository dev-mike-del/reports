from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from report_admin.models import BasicReport


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
        return context