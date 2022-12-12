from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', account_list, name='account_list'),
    path('<str:pk>/', account_profile, name='account_profile'),
]
