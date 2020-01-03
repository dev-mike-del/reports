from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

app_name = 'accounts'


urlpatterns = [

    path('login/', 
    	auth_views.LoginView.as_view(),
    	name='login',
    	),

    path('logout/', 
    	views.logout_request,
    	name='logout',
    	),

    path('profile/', 
    	views.ProflieListView.as_view(),
    	name='profile',
    	),

    path('signup/', views.SignUpView.as_view(), name='signup'),

]