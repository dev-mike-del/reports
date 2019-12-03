from django.shortcuts import render
from django.views.generic import ListView

from report_types.models import BasicReport


class ProflieListView(ListView):
	"""docstring for ProflieListView"""
	model = BasicReport
	