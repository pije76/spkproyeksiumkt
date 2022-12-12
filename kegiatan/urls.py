from django.urls import path, re_path, include

from .views import *

app_name='kegiatan'

urlpatterns = [
    path('', daftar_kegiatan, name="daftar_kegiatan"),
    path('tambah-kegiatan/', tambah_kegiatan, name="tambah_kegiatan"),
    path('standar-deviasi-kegiatan/', standar_deviasi_kegiatan, name="standar_deviasi_kegiatan"),
    path('varians-kegiatan/', varians_kegiatan, name="varians_kegiatan"),
    path('hasil-estimasi-waktu/', daftar_estimasi_waktu, name="daftar_estimasi_waktu"),
    path('estimasi-waktu/', estimasi_waktu, name="estimasi_waktu"),
    path('critical-path/', critical_path, name='critical_path'),
    path('hasil-estimasi-biaya/', daftar_estimasi_biaya, name="daftar_estimasi_biaya"),
    path('estimasi-biaya/', estimasi_biaya, name="estimasi_biaya"),
]
