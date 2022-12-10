from django.urls import path, re_path, include

from .views import *

app_name='proyek'

urlpatterns = [
    path('', proyek_list, name="proyek_list"),
    # path('estimasi-biaya/', estimasi_biaya, name="estimasi_biaya"),
    # path('hasil-estimasi/', hasil_estimasi, name="hasil_estimasi"),
]
