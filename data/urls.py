from django.urls import path, re_path, include

from .views import *

app_name='data'

urlpatterns = [
    path('', data_list, name="data_list"),
    path('kumpul-data/', kumpul_data, name="kumpul_data"),
    path('analisa-data/', analisa_data, name="analisa_data"),
]
