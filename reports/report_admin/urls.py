from django.urls import path

from report_admin import views

app_name = 'report_admin'

urlpatterns = [

    path('comment/<slug>', 
        views.ReportCommentView.as_view(),
        name='comment'),

    path('create', 
        views.ReportCreateView.as_view(),
        name='create'),

    path('preview/<slug>', 
        views.ReportPreviewView.as_view(),
        name='preview'),

    path('update/<slug>', 
        views.ReportUpdateView.as_view(),
        name='update'),

]