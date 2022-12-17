from django import forms
from django.contrib.auth.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _

from .models import *
from kegiatan.models import *


######################################################################################################
class Data_Form(forms.Form):

    user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))


class Data_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Data
        fields = ('user', 'proyek', 'waktu', 'biaya')
        widgets = {
            # 'user': forms.HiddenInput(),
        }


class Kegiatan_Form(forms.Form):
    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    nama_kegiatan = forms.CharField(required=False, label="Nama Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    kode = forms.CharField(required=False, label="Kode Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    bobot_kegiatan = forms.CharField(required=False, label="Bobot Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    estimasi_biaya = forms.CharField(required=False, label="Schedule:", widget=forms.TextInput(attrs={'class': "form-control"}))
    estimasi_waktu = forms.CharField(required=False, label="Tipe Estimasi:", widget=forms.TextInput(attrs={'class': "form-control"}))
