from django.shortcuts import render
from django.views.generic import FormView

from report_admin.forms import BasicReportForm


class BasicReportFormView(FormView):
    """docstring for BasicReportForm"""
    template_name = "report_admin/basicreport_form.html"
    form_class = BasicReportForm
    success_url = ''
