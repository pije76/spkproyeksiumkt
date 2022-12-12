from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _

from .models import *


class Kegiatan_Form(forms.Form):

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    nama_kegiatan = forms.CharField(required=False, label="Nama Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    kode = forms.CharField(required=False, label="Kode Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    predecessor = forms.CharField(required=False, label="Predecessor:", widget=forms.TextInput(attrs={'class': "form-control"}))
    hubungan_keterkaitan = forms.CharField(required=False, label="Hubungan Keterkaitan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    bobot_kegiatan = forms.CharField(required=False, label="Bobot Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    estimasi_biaya = forms.CharField(required=False, label="Perkiraan Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))
    estimasi_waktu = forms.CharField(required=False, label="Tipe Estimasi:", widget=forms.TextInput(attrs={'class': "form-control"}))


class Kegiatan_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Kegiatan
        fields = '__all__'
        # fields = ('proyek', 'nama_kegiatan', 'bobot_kegiatan')
        widgets = {
            # 'user': forms.HiddenInput(),
        }


class EstimasiBiaya_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Estimasi_Biaya
        fields = ('kegiatan', 'estimasi_biaya')
        widgets = {
            # 'user': forms.HiddenInput(),
        }


class EstimasiWaktu_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Estimasi_Waktu
        fields = '__all__'
        # fields = ('kegiatan', 'tipe_estimasi', 'estimasi_waktu')
        widgets = {
            # 'user': forms.HiddenInput(),
        }
