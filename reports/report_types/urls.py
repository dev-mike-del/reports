from django.urls import path

from report_types.views import (BasicReportFormView, )

app_name = 'reports'

urlpatterns = [

    path('form', 
        BasicReportFormView.as_view(),
        name='form'),

]