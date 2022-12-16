from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _

from .models import *

class Proyek_Form(forms.Form):

    user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
    nama_proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    spk = forms.CharField(required=False, label="SPK:", widget=forms.TextInput(attrs={'class': "form-control"}))
    rab = forms.FloatField(required=False, label="RAB:", max_value=1000000000, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "1.00"}))


class Proyek_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    user = forms.CharField(required=False, label="User:", widget=forms.TextInput(attrs={'class': "form-control"}))
    nama_proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    spk = forms.CharField(required=False, label="SPK:", widget=forms.TextInput(attrs={'class': "form-control"}))
    rab = forms.FloatField(required=False, label="Biaya Kegiatan:", max_value=1000000000, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "1.00"}))

    class Meta:
        model = Proyek
        fields = '__all__'
        # fields = ('user', 'nama_proyek', 'spk')
        widgets = {
            # 'user': forms.HiddenInput(),
            # 'tanggal_mulai': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

