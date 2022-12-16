from django.urls import path, re_path, include

from .views import *

app_name='data'

urlpatterns = [
    path('', tabel_data, name="tabel_data"),
    path('tambah-data/', tambah_data, name="tambah_data"),
    path('tambah-data-kegiatan/', tambah_data_kegiatan, name="tambah_data_kegiatan"),
]
