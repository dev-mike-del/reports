from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView, 
    UpdateView, 
    DetailView, 
    ListView, 
    FormView,
    TemplateView
    )

from report_admin.forms import (
    BasicReportForm, 
    BasicReportCommentForm, 
    ReportSearchForm,
    )
from report_admin.models import BasicReport, BasicReportVersion

from status.models import Status
from subscriptions.models import Subscriber
from tags.models import Tag


### Statuses ###
edit, created = Status.objects.get_or_create(title="edit")
sent_for_review, created = Status.objects.get_or_create(title="sent_for_review")
sent_for_edit, created = Status.objects.get_or_create(title="sent_for_edit")
review, created = Status.objects.get_or_create(title="review")
published, created = Status.objects.get_or_create(title="published")
archived, created = Status.objects.get_or_create(title="archived")
confirm, created = Status.objects.get_or_create(title="confirm")


class ReportCreateView(
    LoginRequiredMixin,
    CreateView
    ):
    """docstring for BasicReportCreateView"""
    template_name = 'report_admin/basicreport_form.html'
    model = BasicReport
    form_class = BasicReportForm

    def get_form_kwargs(self):
        kwargs = super(ReportCreateView, self).get_form_kwargs()
        kwargs['initial'].update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReportCreateView,
            self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
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
            if (report.status == sent_for_edit or
                report.status == sent_for_review or
                report.status == confirm):
                report.status = edit
            report.save()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReportUpdateView,
            self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        report = self.object
        context['report'] = report
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        if self.request.user == report.author:
            return context
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        try:
            report = get_object_or_404(BasicReport,
                                        id=context['object'].id)
            if report.status == review:
                messages.warning(self.request, '{} has started proofing {}'.format(report.reviewer, report))
                return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )
        except TypeError:
            pass

        if context is None:
            messages.warning(self.request, 'You are not the author of this report')
            return HttpResponseRedirect(
                reverse('accounts:profile')
                )
        else:
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
        context["report_versions"] = BasicReportVersion.objects.filter(
            basic_report_unique_id=context['object'].unique_id
            ).order_by('-version')
        context['report_tags'] = context['object'].tags_as_string.split(",")
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        if self.request.user == context['object'].author:
            if context['object'].status == published:
                context['object'].status = confirm
                context['object'].save()
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

        if "typo" in self.request.POST:
            report.typo_update = True
            report.save()
            return HttpResponseRedirect(
                reverse('report_admin:update',
                    kwargs={'slug': report.slug}))

        if "update" in self.request.POST:
            report.update = True
            report.save()
            return HttpResponseRedirect(
                reverse('report_admin:update',
                    kwargs={'slug': report.slug}))

        if "cancel" in self.request.POST:
            report.cancel_recall = True
            report.status = published
            report.save()
            messages.success(
                self.request,
                "You have canceled the recall of {}".format(
                                    self.object
                                    )
                )
            return HttpResponseRedirect(reverse(
                                        'list',)
                                        )

        if "make_comments" in self.request.POST:
            report.save()
            return HttpResponseRedirect(
                reverse(
                    'report_admin:comment',
                    kwargs={'slug': report.slug}
                    )
                )

        if "publish" in self.request.POST:
            if report.typo_update:
                pass
            else:
                report.status = published
                report.save()
                tag_obj = []
                tag_obj_messages = []
                subscriber_tags_that_match = []

                if report.tags_as_string:
                    for tag in report.tags_as_string.split(","):
                        tag_object, created = Tag.objects.get_or_create(title=tag.capitalize())
                        report.tags.add(tag_object)

                            
                        tag_obj.append(tag_object)

                # New Test Code 
                for subscriber in Subscriber.objects.all():
                    for tag in subscriber.tags.all():
                        if tag in tag_obj:
                            subscriber_tags_that_match.append(tag)
                    if subscriber_tags_that_match:
                        msg_plain = render_to_string('subscriptions/email.txt', {
                            'user': subscriber.user, 'report': report, 
                            'tags': ", ".join(map(str,subscriber_tags_that_match)),
                            'tags_length':len(subscriber_tags_that_match)})
                        msg_html = render_to_string('subscriptions/email.html', {
                            'user': subscriber.user, 'report': report, 
                            'tags': ", ".join(map(str,subscriber_tags_that_match)),
                            'tags_length':len(subscriber_tags_that_match)})
                        message = EmailMultiAlternatives('New Report from The Report Platform', 
                            msg_plain, settings.EMAIL_HOST_USER, 
                            (subscriber.user.email,),)

                        message.attach_alternative(msg_html, "text/html")


                        tag_obj_messages.append(message)
                        subscriber_tags_that_match = []

                connection = get_connection()
                connection.open()
                connection.send_messages([msg for msg in tag_obj_messages])
                connection.close()
            
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
    context_object_name = 'report'

    def get_form_kwargs(self):
        kwargs = super(ReportCommentView, self).get_form_kwargs()
        report = get_object_or_404(
            BasicReport, id=kwargs['instance'].pk)
        if self.request.user == report.reviewer:
            if report.status == sent_for_edit:
                report.status = review
            report.save()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReportCommentView,
            self).get_context_data(**kwargs)
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        if self.request.user == context['object'].reviewer:
            return context
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        try:
            report = get_object_or_404(BasicReport,
                                        id=context['object'].id)
            if report.status == edit:
                messages.warning(self.request, '{} has started editing {}'.format(report.author, report))
                return HttpResponseRedirect(
                    reverse('accounts:profile')
                    )
        except TypeError:
            pass

        if context is None:
            messages.warning(self.request, 'You are not the reviewer of this report')
            return HttpResponseRedirect(
                reverse('accounts:profile')
                )
        else:
            return super(ReportCommentView, self).render_to_response(
                    context, **response_kwargs
                )



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


class ReportListView(ListView):
    model = BasicReport
    context_object_name = 'reports'

    def get_queryset(self):
        return self.model.objects.filter(status__title='published'
            ).all().order_by('-date_published')

    def get_context_data(self, **kwargs):
        context = super(ReportListView,
            self).get_context_data(**kwargs)
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        return context


class ReportDetailView(DetailView):
    model = BasicReport
    context_object_name = 'report'

    def get_queryset(self):
        return self.model.objects.filter(status__title='published'
            ).all()

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView,
            self).get_context_data(**kwargs)
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        return context


class ReportSearchView(ListView, FormView):
    context_object_name = 'reports'
    model = BasicReport
    form_class = ReportSearchForm
    template_name = 'report_admin/basicreport_search.html'
    paginate_by = 20

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(ReportSearchView, self).get_initial()
        initial['search'] = self.request.GET.get('search')
        initial['from_date'] = self.request.GET.get('from_date')
        initial['to_date'] = self.request.GET.get('to_date')
        initial['tag'] = self.request.GET.get('tag')
        return initial

    def get_context_data(self, **kwargs):
        context = super(ReportSearchView,
            self).get_context_data(**kwargs)
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        return context

    def get_queryset(self):
        print("{}".format("X"*10))
        print(self.request.GET)
        print("{}".format("X"*10))
        object_list = ""

        try:
            search = self.request.GET.get('search')

        except:
            search = ""

        try:
            from_date = self.request.GET.get('from_date')
            from_date = datetime.datetime.strptime(str(from_date), "%m/%d/%Y").date()

        except:
            from_date = None

        try:
            to_date = self.request.GET.get('to_date')
            to_date = datetime.datetime.strptime(str(to_date), "%m/%d/%Y").date()

        except:
            to_date = None 

        try:
            tag = self.request.GET.get('tag')
            tag = get_object_or_404(Tag, title=tag)
        except:
            tag = ""

        try:
            if (search != '' or 
                from_date != None or 
                to_date != None or 
                tag != ""):

                if (search != '' and 
                    from_date != None and 
                    to_date != None and 
                    tag != ''):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__range=(from_date, to_date)),
                            Q(tags=tag),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )

                elif (search != '' and 
                    from_date != None and 
                    to_date != None ):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__range=(from_date, to_date)),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )
                       
                elif (search != '' and 
                    from_date != None and 
                    tag != ''):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__gte=from_date),
                            Q(tags=tag),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )
 
                elif (search != '' and 
                    from_date != None):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__gte=from_date),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )

                elif (search != '' and 
                    to_date != None and 
                    tag != ''):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__lte=to_date),
                            Q(tags=tag),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )

                elif (search != '' and 
                    to_date != None):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(date_published__lte=to_date),
                            Q(search=search)
                            ).all().order_by(
                                '-date_published'
                                )

                elif (tag != '' and 
                    from_date != None and 
                    to_date != None):
                    reports = self.model.objects.filter(
                        Q(status=published),
                        Q(threat_level=threat_level),
                        Q(date_published__range=(from_date, to_date)),
                        Q(tags=tag)).all().order_by('-date_published')

                elif (tag != '' and
                    from_date != None):
                    reports = self.model.objects.filter(
                        Q(status=published),
                        Q(date_published__gte=from_date),
                        Q(tags=tag)).all().order_by('-date_published')

                elif (tag != '' and 
                    to_date != None):
                    reports = self.model.objects.filter(
                        Q(status=published),
                        Q(date_published__lte=to_date),
                        Q(tags=tag)).all().order_by('-date_published')

                elif (tag != ''):
                    reports = self.model.objects.filter(
                        Q(status=published),
                        Q(tags=tag)).all().order_by('-date_published')

                elif (search != ''):
                    reports = self.model.objects.annotate(search=SearchVector(
                        'title', 
                        'executive_summary', 
                        'body', 
                        'conclusion', 
                        'recommendations', 
                        'references',
                        ),).filter(
                            Q(status=published),
                            Q(search=search)
                            ).all().order_by('-date_published')

                else:
                    object_list = None

                try:
                    reports
                except NameError:
                    reports_exists = False
                else:
                    reports_exists = True

                if reports_exists:
                    object_list = reports


                return object_list


        except Exception as e:
            raise e


class AboutView(TemplateView):
    template_name = 'report_admin/basicreport_about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView,
            self).get_context_data(**kwargs)
        try:
            subscriber = get_object_or_404(Subscriber,
                                user=self.request.user)
            context['subscriber'] = subscriber
        except Exception:
            pass
        return context