from django.urls import path

from report_admin import views

app_name = 'report_admin'

urlpatterns = [

    path('form', 
        views.BasicReportFormView.as_view(),
        name='basic_report_form_view'),

    path('preview', 
        views.BasicReportPreviewView.as_view(),
        name='basic_report_preview_view'),

]