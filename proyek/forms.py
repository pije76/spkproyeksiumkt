from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _

from .models import *

class Proyek_Form(forms.Form):

    user = forms.CharField(required=False, label="User:", widget=forms.TextInput(attrs={'class': "form-control"}))
    nama_proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    tanggal_mulai = forms.DateField(required=False, label="Tanggal Mulai:", widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': "form-control"}))
    tanggal_selesai = forms.DateField(required=False, label="Tanggal Selesai:", widget=forms.DateInput(format=('%d-%m-%Y'),attrs={'type': 'date', 'class': "form-control"}))
    spk = forms.CharField(required=False, label="SPK:", widget=forms.TextInput(attrs={'class': "form-control"}))


class Proyek_ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    user = forms.CharField(required=False, label="User:", widget=forms.TextInput(attrs={'class': "form-control"}))
    # user = forms.ChoiceField(label='User', widget=forms.Select, choices="")
    nama_proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
    tanggal_mulai = forms.DateField(required=False, label="Tanggal Mulai:", widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': "form-control"}))
    tanggal_selesai = forms.DateField(required=False, label="Tanggal Selesai:", widget=forms.DateInput(format=('%d-%m-%Y'),attrs={'type': 'date', 'class': "form-control"}))
    spk = forms.CharField(required=False, label="SPK:", widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Proyek
        fields = '__all__'
        # fields = ('user', 'nama_proyek', 'spk')
        widgets = {
            # 'user': forms.HiddenInput(),
            # 'tanggal_mulai': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

