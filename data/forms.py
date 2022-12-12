from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _

from .models import *

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

