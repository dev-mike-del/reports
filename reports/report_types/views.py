from django.shortcuts import render
from django.views.generic import FormView

from report_types.forms import BasicReportForm


class BasicReportFormView(FormView):
	"""docstring for BasicReportForm"""
	template_name = 'basic_report_form.html'
	form_class = BasicReportForm
	success_url = ''
