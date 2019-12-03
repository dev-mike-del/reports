from django.urls import path

from report_admin.views import (BasicReportFormView, )

app_name = 'report_admin'

urlpatterns = [

    path('form', 
        BasicReportFormView.as_view(),
        name='form'),

]