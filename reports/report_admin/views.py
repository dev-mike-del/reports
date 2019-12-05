from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import warning
from django.shortcuts import render
from django.views.generic import FormView, DetailView

from report_admin.forms import BasicReportForm
from report_admin.models import BasicReport, BasicReportVersion

from tags.models import Tag


class BasicReportFormView(
    LoginRequiredMixin,
    FormView
    ):
    """docstring for BasicReportCreateView"""
    template_name = "report_admin/basicreport_form.html"
    form_class = BasicReportForm

    def get_form(self, form_class, **kwargs):
        try:
            obj = kwargs['object']
            report = BasicReport.objects.get(id=obj.id)
            return form_class(instance=report, **self.get_form_kwargs())
        except BasicReport.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(BasicReportUpdateView,
            self).get_context_data(**kwargs)
        report = kwargs['object']
        # report = get_object_or_404(BasicReport,
        #                             id=self.kwargs['pk'])
        request_user = self.request.user
        author = report.author
        reviewer = report.reviewer
        status = report.status

        context['tags'] = Tag.objects.all()
        context['threat_tags'] = report.tags_as_string.split(",")
        context["report_version"] = BasicReportVersion.objects.all()
        context["request_user"] = request_user
        context['report'] = report
        context["author"] = author
        context["reviewer"] = reviewer

        return context

        if request_user == author:
            return context
        elif request_user == reviewer:
            return context
        else:
            return None

    def form_valid(self, form):
        report = form.save(commit=False)
        request_user = self.request.user
        if report.version < .01:
            report.status = first_draft
            report.author = self.request.user
            report.author_as_string = self.request.user

        author = report.author
        reviewer = report.reviewer

        if "save_report" in self.request.POST:
            if request_user == author:
                report.status = edit
            elif request_user == reviewer:
                report.status = review
            report.save()
            return HttpResponseRedirect(
              reverse(
                  'reports_admin:basic_report_form_view',
                  kwargs={'pk': report.pk}
                  )
              )

        if "save_and_preview_report" in self.request.POST:
            report.status = edit
            report.save()
            return HttpResponseRedirect(
                reverse(
                    'reports_admin:basic_report_preview_view',
                    kwargs={'pk': report.pk}
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
                    reverse('reports_admin:basic_report_preview_view',
                                kwargs={'pk': report.pk}))

        if "delete_draft" in self.request.POST:
            report.status = archived
            report.save()
            return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )

    def render_to_response(self, context, **response_kwargs):
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
        return super(BasicReportFormView, self).render_to_response(
            context, **response_kwargs
        )


class BasicReportPreviewView(
    LoginRequiredMixin,
    FormView, 
    DetailView
    ):
    model = BasicReport
    template_name = 'report_admin/basicreport_preview.html'

    def get_form_kwargs(self):
        kwargs = super(BasicReportPreviewView, self).get_form_kwargs()
        pk = kwargs['instance'].pk
        report = get_object_or_404(BasicReport, id=pk)
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
        context['tags'] = report.tags_as_string.split(",")

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
        return super(BasicReportPreviewView, 
            self).render_to_response(context,**response_kwargs)


    def form_valid(self, form):
        report = form.save(commit=False)
        if "edit" in self.request.POST:
            return HttpResponseRedirect(
                reverse('report_admin:basic_report_form_view',
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
            report.status = review
            report.save()
            return HttpResponseRedirect(reverse(
                                        'report_admin:basic_report_form_view',
                                        kwargs={'pk': report.pk})
                                        )

        if "publish" in self.request.POST:
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

