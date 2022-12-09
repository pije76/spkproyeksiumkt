from django.contrib import admin

from .models import *

# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'nama_data',
        'waktu',
        'biaya',
    ]
    # list_filter=['available','created','updated']
    list_editable = [
        'nama_data',
        'waktu',
        'biaya',
    ]

admin.site.register(Data, DataAdmin)
