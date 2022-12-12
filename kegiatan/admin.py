from django.contrib import admin

from .models import *

# Register your models here.

class KegiatanAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'proyek',
        'nama_kegiatan',
        'kode',
        'predecessor',
        'hubungan_keterkaitan',
        'bobot_kegiatan',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'nama_kegiatan',
        'kode',
        'predecessor',
        'hubungan_keterkaitan',
        'bobot_kegiatan',
    ]

class Estimasi_WaktuAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'kegiatan',
        'estimasi_waktu_a',
        'estimasi_waktu_m',
        'estimasi_waktu_b',
        'expected_duration',
        'standar_deviasi',
        'varians_kegiatan',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'kegiatan',
        'estimasi_waktu_a',
        'estimasi_waktu_m',
        'estimasi_waktu_b',
    ]

class Estimasi_BiayaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'kegiatan',
        'estimasi_biaya',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'kegiatan',
        'estimasi_biaya',
    ]

admin.site.register(Kegiatan, KegiatanAdmin)
admin.site.register(Estimasi_Waktu, Estimasi_WaktuAdmin)
admin.site.register(Estimasi_Biaya, Estimasi_BiayaAdmin)

