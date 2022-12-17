from django import forms
from django.contrib.auth.models import *
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import *


class Kegiatan_ModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
	# proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))
	bobot_kegiatan = forms.FloatField(required=False, label="Bobot Kegiatan:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.10"}))
	biaya_kegiatan = forms.FloatField(required=False, label="Biaya Kegiatan:", max_value=1000000000, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "50000.0"}))

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

class PERT_ModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
	# proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))
	optimistic_time = forms.FloatField(required=False, label="Optimistic Time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	most_likely_time = forms.FloatField(required=False, label="Most Likely Time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	pessimistic_time = forms.FloatField(required=False, label="Pessimistic Time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))

	class Meta:
		model = PERT
		# fields = '__all__'
		fields = (
			'kegiatan',
			'optimistic_time',
			'most_likely_time',
			'pessimistic_time',
			# 'duration',
		)
		widgets = {
			# 'user': forms.HiddenInput(),
		}

class CPM_ModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
	# proyek = forms.CharField(required=False, label="Proyek:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# waktu = forms.CharField(required=False, label="Waktu:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# biaya = forms.CharField(required=False, label="Biaya:", widget=forms.TextInput(attrs={'class': "form-control"}))
	# optimistic_time = forms.FloatField(required=False, label="Optimistic Time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	# most_likely_time = forms.FloatField(required=False, label="most_likely_time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	# pessimistic_time = forms.FloatField(required=False, label="Pessimistic Time:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	# predecessor = forms.CharField(required=False, label="Predecessor:", widget=forms.TextInput(attrs={'class': "form-control"}))
	predecessor = forms.ChoiceField(choices=PREDECESSOR_CHOICES, required=False, label="Predecessor:", widget=forms.Select(attrs={'class': "form-control"}))
	hubungan_keterkaitan = forms.ChoiceField(choices=KONSTRAIN_CHOICES, required=False, label="Hubungan Keterkaitan:", widget=forms.Select(attrs={'class': "form-control"}))
	# hubungan_keterkaitan = forms.ModelChoiceField(queryset=ModelName.objects.all())

	class Meta:
		model = CPM
		# fields = '__all__'
		fields = (
			'kegiatan',
			'predecessor',
			'hubungan_keterkaitan',
		)
		widgets = {
			# 'user': forms.HiddenInput(),
		}


class Schedule_ModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# user = forms.CharField(required=False, label="User:", widget=forms.HiddenInput(attrs={'class': "form-control"}))
	# kegiatan = forms.CharField(required=False, label="Kegiatan:", widget=forms.TextInput(attrs={'class': "form-control"}))
	minggu = forms.FloatField(required=False, label="Minggu:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "1.0"}))
	acwp = forms.FloatField(required=False, label="ACWP:", max_value=1000000000, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "50000.0"}))
	progress_rencana = forms.FloatField(required=False, label="Progress Rencana:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))
	progress_aktual = forms.FloatField(required=False, label="Progress Aktual:", max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}))


	class Meta:
		model = Schedule
		# fields = '__all__'
		fields = (
			# 'kegiatan',
			'minggu',
			'acwp',
			'progress_rencana',
			'progress_aktual',
		)
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
		model = Schedule
		fields = '__all__'
		# fields = (
			# 'kegiatan',
			# 'estimasi_biaya',
		# )
		widgets = {
			# 'user': forms.HiddenInput(),
		}

