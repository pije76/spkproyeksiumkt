from django.urls import path, re_path, include

from .views import *

app_name='proyek'

urlpatterns = [
    path('', daftar_proyek, name="daftar_proyek"),
    path('tambah-proyek/', tambah_proyek, name="tambah_proyek"),
]
