from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import warning
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView

from report_admin.forms import BasicReportForm
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
        report.author_as_string = self.request.user
        report.reviewer_as_string = report.reviewer
        report.save()

        if "save_report" in self.request.POST:
            return HttpResponseRedirect(
              reverse(
                  'report_admin:update',
                  kwargs={'slug': report.slug}
                  )
              )
        elif "save_and_preview_report" in self.request.POST:
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
    def render_to_response(self, context, **response_kwargs):
        try:
            report = get_object_or_404(BasicReport,
                                        id=self.kwargs['pk'])
            reviewer = report.reviewer
            if context is None:
                if self.request.user == report.author:
                    warning(self.request, '{} has started proofing {}'.format(reviewer, report))
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

    def get_form_kwargs(self):
        kwargs = super(ReportPreviewView, self).get_form_kwargs()
        report = get_object_or_404(
            BasicReport, id=kwargs['instance'].pk)
        request_user = self.request.user
        reviewer = report.reviewer

        if reviewer == request_user:
            if report.status == sent_for_review:
                report.status = review
            report.save()

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BasicReportPreviewView,
            self).get_context_data(**kwargs)
        report = kwargs['object']
        context["version"] = BasicReportVersion.objects.all()
        context['report'] = report
        context["author"] = report.author
        context["reviewer"] = report.reviewer
        context['report_tags'] = report.tags_as_string.split(",")

        if self.request.user == report.author:
            return context
        elif self.request.user == report.reviewer:
            return context
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        report = get_object_or_404(BasicReport, id=self.kwargs['pk'])
        if context is None:
            if report.reviewer == self.request.user:
                warning(self.request, '{} has recalled {}'.format(report.author, report))
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
                    kwargs={'pk': report.pk}))

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
                                        'report_admin:update',
                                        kwargs={'pk': report.pk})
                                        )

        if "publish" in self.request.POST:
            for tag in threat.tags_str.split(","):
                tag_object, created = Tag.objects.get_or_create(title=tag)
                report.tags.add(tag_object)
            report.status = published
            report.save()
            report.save_m2m()
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
    template_name = "report_admin/basicreport_form.html"
    model = BasicReport
    fields = [
        'reviewer',
        'title',
        'title_peer_review', 
        'executive_summary',
        'executive_summary_peer_review', 
        'introduction',
        'introduction_peer_review', 
        'body',
        'body_peer_review',
        'conclusion',
        'conclusion_peer_review',
        'recommendations',
        'recommendations_peer_review',
        'references',
        'references_peer_review',
        'tags_as_string',
        'tags_peer_review',
        ]

    def get_context_data(self, **kwargs):
        context = super(ReportUpdateView,
            self).get_context_data(**kwargs)
        request_user = self.request.user
        try:
            report = kwargs['object']
            author = report.author
            reviewer = report.reviewer
            status = report.status
            context['threat_tags'] = report.tags_as_string.split(",")
            context['report'] = report
            context["author"] = author
            context["reviewer"] = reviewer
            context["report_version"] = BasicReportVersion.objects.all()
            if request_user == author:
                return context
            elif request_user == reviewer:
                return context
            else:
                return None
        except KeyError:
            pass

        context["request_user"] = request_user
        context['tags'] = Tag.objects.all()
        
        return context

    def form_valid(self, form):
        report = form.save(commit=False)

        if "save_report" in self.request.POST:
            report.status = edit
            report.save()
            return HttpResponseRedirect(
              reverse(
                  'report_admin:update',
                  kwargs={'object': self}
                  )
              )

        if "save_and_preview_report" in self.request.POST:
            report.status = edit
            report.save()
            return HttpResponseRedirect(
                reverse(
                    'report_admin:preview',
                    kwargs={'object': self}
                    )
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
            report.save()
            return HttpResponseRedirect(
                    reverse('report_admin:preview',
                                kwargs={'pk': report.pk}))

        if "delete_draft" in self.request.POST:
            report.status = archived
            report.save()
            return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )

    def render_to_response(self, context, **response_kwargs):
        try:
            request_user = self.request.user
            report = get_object_or_404(BasicReport,
                                        id=self.kwargs['pk'])
            author = report.author
            reviewer = report.reviewer

            if context is None:
                if author == request_user:
                    warning(self.request, '{} has started proofing {}'.format(reviewer, report))
                    return HttpResponseRedirect(
                        reverse('accounts:profile')
                        )
        except KeyError:
            pass

        return super(ReportUpdateView, self).render_to_response(
                context, **response_kwargs
            )