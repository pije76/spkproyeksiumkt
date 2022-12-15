from django.urls import path, re_path, include

from .views import *

app_name='kegiatan'

urlpatterns = [
    path('', tabel_kegiatan, name="tabel_kegiatan"),
    path('create-cpm-forward/', create_forwardsCPM, name='create_forwardsCPM'),
    path('create-cpm-backward/', create_backwardsCPM, name='create_backwardsCPM'),
    path('export-cpm/', export_excel, name='export_excel'),
    path('tambah-kegiatan/', tambah_kegiatan, name="tambah_kegiatan"),
    path('tabel-estimasi-waktu/', tabel_estimasi_waktu, name="tabel_estimasi_waktu"),
    path('estimasi-waktu/', estimasi_waktu, name="estimasi_waktu"),
    path('tabel-cpm/', tabel_cpm, name='tabel_cpm'),
    path('hasil-estimasi-biaya/', daftar_estimasi_biaya, name="daftar_estimasi_biaya"),
    path('estimasi-biaya/', estimasi_biaya, name="estimasi_biaya"),
]
