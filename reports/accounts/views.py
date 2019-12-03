from django.shortcuts import render
from django.views.generic import ListView

from report_admin.models import BasicReport


class ProflieListView(ListView):
	"""docstring for ProflieListView"""
	model = BasicReport
	template_name = "accounts/profile_list.html"
	