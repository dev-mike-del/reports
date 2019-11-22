from django.views.generic.list import ListView

from report_types.models import BasicReport

class BasicReportListView(ListView):

    model = BasicReport
