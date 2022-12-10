from django.urls import path, re_path, include

from .views import *

app_name='proyek'

urlpatterns = [
    path('', proyek_list, name="proyek_list"),
]
