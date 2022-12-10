from django.contrib import admin

from .models import *

# Register your models here.
class DataProyek(admin.ModelAdmin):
    list_display = [
        'id',
        # 'user',
        'nama_proyek',
        'SPK',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'nama_proyek',
        'SPK',
    ]

admin.site.register(Proyek, DataProyek)
admin.site.register(Estimasi_Waktu)
admin.site.register(PERT)
