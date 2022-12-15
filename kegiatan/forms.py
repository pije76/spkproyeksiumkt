from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import *


class Kegiatan_Form(forms.Form):

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    nama_kegiatan = forms.CharField(required=False, label="Nama Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    kode = forms.CharField(required=False, label="Kode Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    predecessor = forms.CharField(required=False, label="Predecessor:", widget=forms.TextInput(attrs={'class': "form-control"}))
    hubungan_keterkaitan = forms.CharField(required=False, label="Hubungan Keterkaitan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    bobot_kegiatan = forms.CharField(required=False, label="Bobot Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
    estimasi_biaya = forms.CharField(required=False, label="Estimasi Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))
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
        # fields = '__all__'
        fields = (
            'proyek',
            'nama_kegiatan',
            'kode',
            'predecessor',
            'hubungan_keterkaitan',
            'bobot_kegiatan',
            'biaya_kegiatan',
        )
        widgets = {
            # 'user': forms.HiddenInput(),
        }


    proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
    nama_kegiatan = models.CharField(_("Nama Kegiatan"), max_length=255, blank=True, null=True)
    kode = models.CharField(max_length=255, blank=True, null=True)
    predecessor = models.CharField(max_length=255, blank=True, null=True)
    hubungan_keterkaitan = models.CharField(max_length=255, choices=KONSTRAIN_CHOICES, default="ss", null=True, blank=True)
    bobot_kegiatan = models.DecimalField(_("Bobot Kegiatan"), max_digits=3, decimal_places=1, blank=True, null=True)
    biaya_kegiatan = models.DecimalField(_("Biaya Kegiatan"), max_digits=10, decimal_places=0, blank=True, null=True)

    # estimasi_biaya = models.ForeignKey(Estimasi_Biaya, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_biaya_kegiatan')
    # estimasi_waktu = models.ForeignKey(Estimasi_Waktu, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_waktu_kegiatan')
    duration = models.FloatField(_("Expected Duration"), blank=True, null=True)
    standar_deviasi = models.FloatField(_("Standar Deviasi"), blank=True, null=True)
    varians_kegiatan = models.FloatField(_("Varians Kegiatan"), blank=True, null=True)


class EstimasiBiaya_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    # proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Estimasi_Biaya
        fields = (
            'kegiatan',
            # 'estimasi_biaya',
        )
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
        # fields = '__all__'
        fields = (
            'kegiatan',
            'estimasi_waktu_a',
            'estimasi_waktu_m',
            'estimasi_waktu_b',
            # 'duration',
        )
        widgets = {
            # 'user': forms.HiddenInput(),
        }
