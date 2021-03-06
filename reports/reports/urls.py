"""reports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from report_admin.views import (
    ReportListView, 
    ReportDetailView, 
    ReportSearchView,
    AboutView,
    )


urlpatterns = [
    path('', 
        ReportListView.as_view(), 
        name='list',
        ),

    path('about',
        AboutView.as_view(),
        name='about',
        ),

    path('accounts/', include(
            'accounts.urls', 
            namespace='accounts',
            )),

    path('admin/', admin.site.urls),

    path('report_admin/',
        include(
            'report_admin.urls', 
            namespace='report_admin',
            )
        ),

    path('search',
        ReportSearchView.as_view(),
        name='search',
        ),

    path('subscriptions/', include(
            'subscriptions.urls', 
            namespace='subscriptions',
            )),

    path('<slug>', 
        ReportDetailView.as_view(), 
        name='detail',
        ),

]
