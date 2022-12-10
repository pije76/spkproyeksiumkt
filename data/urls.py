from django.urls import path, re_path, include

from .views import *

app_name='data'

urlpatterns = [
    path('', data_list, name="data_list"),
]
