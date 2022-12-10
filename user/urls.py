from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('', account_profile, name='account_profile'),
]
