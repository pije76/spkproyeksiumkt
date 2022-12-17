from django.contrib import admin

from .models import *

# Register your models here.
class KegiatanAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        # 'proyek',
        'nama_kegiatan',
        'kode',
        'predecessor',
        'hubungan_keterkaitan',
        'bobot_kegiatan',
        'biaya_kegiatan',
        'duration',
   ]

    # list_filter=['available','created','updated']
    list_editable = [
        'nama_kegiatan',
        'kode',
        'predecessor',
        'hubungan_keterkaitan',
        'bobot_kegiatan',
        'biaya_kegiatan',
        'duration',
    ]

class PERTAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'kegiatan',
        'optimistic_time',
        'most_likely_time',
        'pessimistic_time',
        'duration',
        'standar_deviasi',
        'varians_kegiatan',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'kegiatan',
        'optimistic_time',
        'most_likely_time',
        'pessimistic_time',
        'duration',
        'standar_deviasi',
        'varians_kegiatan',
    ]

class CPMAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'kegiatan',
        'kode',
        'duration',
        'predecessor',
        # 'hubungan_keterkaitan',
        'earliest_start',
        'earliest_finish',
        'latest_start',
        'latest_finish',
        'slack_time',
        'critical',
   ]

    # list_filter=['available','created','updated']
    list_editable = [
        'kegiatan',
        'kode',
        'duration',
        'predecessor',
        # 'hubungan_keterkaitan',
        'earliest_start',
        'earliest_finish',
        'latest_start',
        'latest_finish',
        'slack_time',
        'critical',
    ]

class Estimasi_BiayaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'minggu',
        'progress_rencana',
        'progress_aktual',
        'acwp',
        'bcwp',
        'bcws',
        'cost_variance',
        'cost_performance_index',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'minggu',
        'progress_rencana',
        'progress_aktual',
        'acwp',
        'bcwp',
        'bcws',
        'cost_variance',
        'cost_performance_index',
    ]

admin.site.register(Kegiatan, KegiatanAdmin)
admin.site.register(CPM, CPMAdmin)
admin.site.register(PERT, PERTAdmin)
admin.site.register(Estimasi_Biaya, Estimasi_BiayaAdmin)

