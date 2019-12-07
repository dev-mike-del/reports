from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView

from report_admin.forms import BasicReportForm, BasicReportCommentForm
from report_admin.models import BasicReport, BasicReportVersion

from status.models import Status
from tags.models import Tag


### Statuses ###
edit, created = Status.objects.get_or_create(title="edit")
sent_for_review, created = Status.objects.get_or_create(title="sent_for_review")
sent_for_edit, created = Status.objects.get_or_create(title="sent_for_edit")
review, created = Status.objects.get_or_create(title="review")
published, created = Status.objects.get_or_create(title="published")
archived, created = Status.objects.get_or_create(title="archived")


class ReportCreateView(
    LoginRequiredMixin,
    CreateView
    ):
    """docstring for BasicReportCreateView"""
    template_name = 'report_admin/basicreport_form.html'
    model = BasicReport
    form_class = BasicReportForm

    def get_context_data(self, **kwargs):
        context = super(ReportCreateView,
            self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        try:
            report = self.object
            context['report'] = report
            if self.request.user == report.author:
                return context
            else:
                return None
        except AttributeError:
            pass
        return context

    def form_valid(self, form):
        report = form.save(commit=False)
        report.status = edit
        report.author = self.request.user
        report.author_as_string = self.request.user.username
        report.reviewer_as_string = report.reviewer.username
        report.save()

        if "save_report" in self.request.POST:
            return HttpResponseRedirect(
              reverse(
                  'report_admin:update',
                  kwargs={'slug': report.slug}
                  )
              )
        elif "preview_report" in self.request.POST:
            return HttpResponseRedirect(
                reverse(
                    'report_admin:preview',
                    kwargs={'slug': report.slug}
                    )
                )

    
class ReportUpdateView(
    ReportCreateView,
    UpdateView
    ):
    """docstring for BasicReportCreateView"""
    def get_form_kwargs(self):
        kwargs = super(ReportUpdateView, self).get_form_kwargs()
        report = get_object_or_404(
            BasicReport, id=kwargs['instance'].pk)
        if self.request.user == report.author:
            if report.status == sent_for_edit:
                report.status = edit
            report.save()
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        try:
            report = get_object_or_404(BasicReport,
                                        id=self.kwargs['pk'])
            reviewer = report.reviewer
            if context is None:
                if self.request.user == report.author:
                    messages.warning(self.request, '{} has started proofing {}'.format(reviewer, report))
                    return HttpResponseRedirect(
                        reverse('accounts:profile')
                        )
        except KeyError:
            pass

        return super(ReportUpdateView, self).render_to_response(
                context, **response_kwargs
            )


class ReportPreviewView(
    LoginRequiredMixin,
    UpdateView,
    DetailView
    ):
    model = BasicReport
    template_name = 'report_admin/basicreport_preview.html'
    fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super(ReportPreviewView, self).get_form_kwargs()
        report = get_object_or_404(
            BasicReport, id=kwargs['instance'].pk)
        if self.request.user == report.reviewer:
            if report.status == sent_for_review:
                report.status = review
            report.save()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReportPreviewView,
            self).get_context_data(**kwargs)
        if self.request.user == context['object'].author:
            return context
        elif self.request.user == context['object'].reviewer:
            return context
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        report = get_object_or_404(BasicReport, id=context['object'].id)
        if context is None:
            if report.reviewer == self.request.user:
                messages.warning(self.request, '{} has recalled {}'.format(report.author, report))
                return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )
        return super(ReportPreviewView, 
            self).render_to_response(context,**response_kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)

        if "edit" in self.request.POST:
            return HttpResponseRedirect(
                reverse('report_admin:update',
                    kwargs={'slug': report.slug}))

        if "submit_for_review" in self.request.POST:
            report.status = sent_for_review
            report.save()
            messages.success(
                self.request,
                "Your report has been saved and has been sent to {} for review.".format(
                                    self.object.reviewer.first_name
                                    )
                )
            return HttpResponseRedirect(reverse('accounts:profile'))

        if "make_comments" in self.request.POST:
            return HttpResponseRedirect(reverse(
                                        'report_admin:comment',
                                        kwargs={'slug': report.slug})
                                        )

        if "publish" in self.request.POST:
            if report.tags_as_string:
                for tag in report.tags_as_string.split(","):
                    tag_object, created = Tag.objects.get_or_create(title=tag)
                    report.tags.add(tag_object)
            report.status = published
            report.save()
            messages.success(
                self.request,
                "{} has been published.".format(
                                    self.object
                                    )
                )
            return HttpResponseRedirect(reverse(
                                        'accounts:profile',
                                        )
            )



class ReportCommentView(
    LoginRequiredMixin,
    UpdateView
    ):
    """docstring for BasicReportCreateView"""
    template_name = "report_admin/basicreport_comment.html"
    model = BasicReport
    form_class = BasicReportCommentForm

    def get_context_data(self, **kwargs):
        context = super(ReportCommentView,
            self).get_context_data(**kwargs)
        if self.request.user == context['object'].reviewer:
            return context
        else:
            return None

    def form_valid(self, form):
        report = form.save(commit=False)
        if "save" in self.request.POST:
            report.save()
            return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )

        if "send_comments_to_author" in self.request.POST:
            report.status = sent_for_edit
            report.save()
            messages.success(
                self.request,
                "Your comments have been sent to {}.".format(
                                    self.object.author.first_name
                                    )
                )
            return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )

        if "back" in self.request.POST:
            return HttpResponseRedirect(
                    reverse('report_admin:preview',
                                kwargs={'slug': report.slug}))

