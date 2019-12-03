from django.shortcuts import render
from django.views.generic import FormView

from report_types.forms import BasicReportForm


class BasicReportFormView(FormView):
    """docstring for BasicReportForm"""
    template_name = "report_types/basicreport_form.html"
    form_class = BasicReportForm
    success_url = ''
