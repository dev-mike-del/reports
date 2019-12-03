from django.views.generic.list import ListView

from report_admin.models import BasicReport

class BasicReportListView(ListView):

    model = BasicReport
