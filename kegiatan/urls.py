from django.urls import path, re_path, include

from .views import *

app_name='kegiatan'

urlpatterns = [
    path('', tabel_kegiatan, name="tabel_kegiatan"),
    # path('create-forward-cpm/', create_forwardsCPM, name='create_forwardsCPM'), # create dari Python
    # path('create-backward-cpm/', create_backwardsCPM, name='create_backwardsCPM'), # create dari Python
    path('create-cpm/', create_cpm, name='create_cpm'), # create dari Python
    path('export-cpm/', export_excel, name='export_excel'),
    path('tambah-kegiatan/', tambah_kegiatan, name="tambah_kegiatan"),
    path('tabel-pert/', tabel_pert, name="tabel_pert"),
    path('tambah-pert/', tambah_pert, name="tambah_pert"),
    path('tabel-cpm/', tabel_cpm, name='tabel_cpm'),
    path('tambah-cpm/', tambah_cpm, name='tambah_cpm'),
    path('table-biaya/', tabel_estimasi_biaya, name="tabel_estimasi_biaya"),
    # path('estimasi-biaya/', estimasi_biaya, name="estimasi_biaya"),
    path('tabel-schedule/', tabel_schedule, name="tabel_schedule"), # formset 2 input progress + 1 input minggu
    path('tambah-schedule/', tambah_schedule, name="tambah_schedule"),
]
