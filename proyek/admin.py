from django.contrib import admin

from .models import *

# Register your models here.
class ProyekAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'nama_proyek',
        'tanggal_mulai',
        'tanggal_selesai',
        'spk',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'nama_proyek',
        'tanggal_mulai',
        'tanggal_selesai',
        'spk',
    ]
admin.site.register(Proyek, ProyekAdmin)
