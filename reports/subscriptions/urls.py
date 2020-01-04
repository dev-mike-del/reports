from django.urls import path

from . import views

app_name = 'subscriptions'

urlpatterns = [

    path('settings', 
        views.SubscriptionsCreateView.as_view(),
        name='create'),

    path('settings/<subscriber_slug>', 
        views.SubscriptionsUpdateView.as_view(),
        name='settings'),

    path('success', 
        views.SubscriptionsCreateViewSuccess.as_view(),
        name='subscriptions_create_view_success'),

    path('unsubscribe/<subscriber_slug>', 
        views.SubscriptionsDeleteView.as_view(),
        name='subscriptions_delete_view'),

    path('unsubscribe_confirmation', 
        views.SubscriptionsDeleteViewSuccess.as_view(),
        name='subscriptions_delete_view_success'),

    path('updated', 
        views.SubscriptionsUpdateViewSuccess.as_view(),
        name='subscriptions_update_view_success'),

]
