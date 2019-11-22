from django.urls import path

from report_types.views import (Form, )

app_name = 'reports'

urlpatterns = [

    path('form', 
        Form.as_view(),
        name='form'),

]