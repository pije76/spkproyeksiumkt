from django.urls import path, re_path, include

from .views import *

app_name='data'

urlpatterns = [
    path('', daftar_data, name="daftar_data"),
    path('tambah-data/', tambah_data, name="tambah_data"),
    path('analisa-data/', analisa_data, name="analisa_data"),
]
