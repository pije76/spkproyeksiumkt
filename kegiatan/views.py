from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *
from .cpm import *

from proyek.models import *
from proyek.forms import *
from accounts.models import *

import re
import pandas as pd
import numpy as np
import math
import xlwt
import itertools

# Create your views here.
################################# KEGIATAN ########################################
@login_required()
def tabel_kegiatan(request):
	page_title = _('Daftar Kegiatan')
	data_user =   UserProfile.objects.all()
	data_kegiatan = Kegiatan.objects.filter()
	total_bobot = Kegiatan.objects.aggregate(Sum('bobot_kegiatan'))
	total_biaya = Kegiatan.objects.aggregate(Sum('biaya_kegiatan'))
	proyek_types = Proyek.objects.all()

	project_id = request.GET.get('project')

	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
		'total_bobot': total_bobot,
		'total_biaya': total_biaya,
		'proyek_types': proyek_types,
	}

	return render(request,'kegiatan/tabel_kegiatan.html', context)


#@login_required()
def tambah_kegiatan(request):
	page_title = _('Tambah Kegiatan')
	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_kegiatan = Kegiatan.objects.filter()
	data_rab =   Kegiatan.objects.all().values_list("biaya_kegiatan")

	if request.method == 'POST':
		form = Kegiatan_ModelForm(request.POST or None)

		if form.is_valid():
			profile = form.save(commit=False)
			profile.proyek = form.cleaned_data['proyek']
			profile.nama_kegiatan = form.cleaned_data['nama_kegiatan']
			profile.kode = form.cleaned_data['kode']
			profile.bobot_kegiatan = form.cleaned_data['bobot_kegiatan']
			profile.biaya_kegiatan = form.cleaned_data['biaya_kegiatan']
			profile.predecessor = form.cleaned_data['predecessor']
			profile.hubungan_keterkaitan = form.cleaned_data['hubungan_keterkaitan']
			profile.save()

			messages.success(request, _('Your Kegiatan has been save successfully.'))
			return redirect('kegiatan:tabel_kegiatan')
		else:
			messages.warning(request, form.errors)

	else:
		form = Kegiatan_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
		'form': form,
	}

	return render(request,'kegiatan/tambah_kegiatan.html', context)


############################### PERT ######################################
def hitungDurasi(a,m,b):
	return (a + (4*m) + b)/6


def hitungDeviasi(a,b):
	return (b-a)/6


def hitungVarians(a,b):
	return pow((b-a)/6,2)


def tabel_pert(request):
	page_title = _('Daftar PERT')
	data_user =   UserProfile.objects.all()
	pert_data = PERT.objects.all()
	total_estimasi_waktu = PERT.objects.aggregate(Sum('duration'))
	total_duration = PERT.objects.aggregate(Sum('duration'))
	varians_kegiatan = PERT.objects.aggregate(Sum('varians_kegiatan'))

	if varians_kegiatan:standar_varians_kejadian = varians_kegiatan.values()
	standar_varians_kejadian = list(varians_kegiatan.values())
	standar_varians_kejadian = standar_varians_kejadian[0]
	if standar_varians_kejadian is None:
		standar_deviasi_kejadian = 0
	else:
		standar_deviasi_kejadian = math.sqrt(standar_varians_kejadian)

	optimistic_time = PERT.objects.all().values_list("optimistic_time")
	most_likely_time = PERT.objects.all().values_list("most_likely_time")
	pessimistic_time = PERT.objects.all().values_list("pessimistic_time")

	optimistic_time = [item for item in optimistic_time]
	most_likely_time = [item for item in most_likely_time]
	pessimistic_time = [item for item in pessimistic_time]

	context = {
		'page_title': page_title,
		'pert_data': pert_data,
		'total_estimasi_waktu': total_estimasi_waktu,
		'optimistic_time': optimistic_time,
		'most_likely_time': most_likely_time,
		'pessimistic_time': pessimistic_time,
		'total_duration': total_duration,
		'varians_kegiatan': varians_kegiatan,
		'standar_deviasi_kejadian': standar_deviasi_kejadian,
	}

	return render(request,'kegiatan/tabel_pert.html', context)


#@login_required()
def tambah_pert(request):
	page_title = _('Tambah PERT')

	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_proyek =   Proyek.objects.filter(user=user_id)

	data_rab = Kegiatan.objects.aggregate(Sum('biaya_kegiatan'))
	data_rab = list(data_rab.values())
	data_rab = data_rab[0]

	duration = PERT.objects.aggregate(Sum('duration'))
	duration = list(duration.values())
	duration = duration[0]

	standar_deviasi = PERT.objects.aggregate(Sum('standar_deviasi'))
	standar_deviasi = list(standar_deviasi.values())
	standar_deviasi = standar_deviasi[0]

	varians_kegiatan = PERT.objects.aggregate(Sum('varians_kegiatan'))
	varians_kegiatan = list(varians_kegiatan.values())
	varians_kegiatan = varians_kegiatan[0]

	if request.method == 'POST':
		form = PERT_ModelForm(request.POST or None)

		if form.is_valid():
			estimasi = form.save(commit=False)

			get_select = request.POST.get('kegiatan')
			estimasi.kegiatan = Kegiatan.objects.get(id=get_select)
			estimasi.optimistic_time = form.cleaned_data['optimistic_time']
			estimasi.most_likely_time = form.cleaned_data['most_likely_time']
			estimasi.pessimistic_time = form.cleaned_data['pessimistic_time']
			hitung_Durasi = hitungDurasi(estimasi.optimistic_time, estimasi.most_likely_time, estimasi.pessimistic_time)
			estimasi.duration = hitung_Durasi
			hitung_Deviasi = hitungDeviasi(estimasi.optimistic_time, estimasi.pessimistic_time)
			estimasi.standar_deviasi = hitung_Deviasi
			hitung_Varians = hitungVarians(estimasi.optimistic_time, estimasi.pessimistic_time)
			estimasi.varians_kegiatan = hitung_Varians
			estimasi.save()

			save_kegiatan = Kegiatan.objects.get(id=get_select)
			save_kegiatan.duration = hitung_Durasi
			save_kegiatan.save()

			messages.success(request, _('Your PERT has been save successfully.'))
			return redirect('kegiatan:tabel_pert')
		else:
			messages.warning(request, form.errors)

	else:
		form = PERT_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
	}

	return render(request,'kegiatan/tambah_pert.html', context)


################################ CPM ##########################################
def tabel_cpm(request):
	page_title = _('Tabel CPM')
	user_id = request.user.is_authenticated
	data_kegiatan = CPM.objects.all()

	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
	}

	return render(request,'kegiatan/tabel_cpm.html', context)


def tambah_cpm(request):
	page_title = _('Tambah CPM')
	is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

	get_select = request.GET.get('get_select')

	if request.method == 'POST':
		get_select = request.POST.get('get_select')
		form = CPM_ModelForm(request.POST or None)

		if form.is_valid():
			estimasi = form.save(commit=False)

			# estimasi.kegiatan = form.cleaned_data['kegiatan']
			# estimasi.optimistic_time = form.cleaned_data['optimistic_time']
			# estimasi.most_likely_time = form.cleaned_data['most_likely_time']
			# estimasi.pessimistic_time = form.cleaned_data['pessimistic_time']
			# hitung_Durasi = hitungDurasi(estimasi.optimistic_time, estimasi.most_likely_time, estimasi.pessimistic_time)
			# estimasi.duration = hitung_Durasi
			# hitung_Deviasi = hitungDeviasi(estimasi.optimistic_time, estimasi.pessimistic_time)
			# estimasi.standar_deviasi = hitung_Deviasi
			# hitung_Varians = hitungVarians(estimasi.optimistic_time, estimasi.pessimistic_time)
			# estimasi.varians_kegiatan = hitung_Varians
			# estimasi.save()

			# obj, update = PERT.objects.update_or_create(kegiatan=estimasi.kegiatan, optimistic_time=estimasi.optimistic_time, most_likely_time=estimasi.most_likely_time, pessimistic_time=estimasi.pessimistic_time)

			# get_select = request.POST.get('get_select')
			# get_select = estimasi.kegiatan.id
			# set_kegiatan = Kegiatan.objects.get(id=get_select)
			# set_kegiatan.duration = hitung_Durasi
			# set_kegiatan.standar_deviasi = hitung_Deviasi
			# set_kegiatan.varians_kegiatan = hitung_Varians

			# set_kegiatan.save()

			messages.success(request, _('Your PERT has been save successfully.'))
			return redirect('kegiatan:tabel_pert')
		else:
			messages.warning(request, form.errors)

	else:
		form = CPM_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
	}

	return render(request,'kegiatan/tambah_cpm.html', context)


################################## CPM ####################################
def export_excel(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Sheet1')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Nama Kegiatan', 'Kode', 'Predecessor', 'Durasi', 'ES', 'EF', 'LS', 'LF', 'Slack', 'Lintasan', ]

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = Kegiatan.objects.all().values_list('nama_kegiatan', 'kode', 'predecessor', 'duration')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	# wb.save(response)
	wb.save("/var/www/html/spkproyeksiumkt/kegiatan/data.xlsx")
	# return response
	messages.success(request, _('Your CPM table has been saved to data.xlsx successfully.'))
	return redirect('kegiatan:tabel_cpm')


def create_cpm(request):
	main()
	messages.success(request, _('Your CPM has been created successfully.'))
	return redirect('kegiatan:tabel_cpm')


################################ SCHEDULE & BIAYA ##########################################
def tabel_estimasi_biaya(request):
	page_title = _('Daftar Schedule')
	data_user =   UserProfile.objects.all()
	estimasi_biaya = Schedule.objects.filter()
	# total_estimasi_waktu = PERT.objects.aggregate(Sum('duration'))


	if request.method == 'POST':
		form = Proyek_Form(request.POST or None)
		# form = Proyek_ModelForm(request.POST or None)

		if form.is_valid():
			profile = Kegiatan()
			# profile = form.save(commit=False)
			# profile.user = form.cleaned_data['user']
			profile.nama_proyek = form.cleaned_data['nama_proyek']
			profile.spk = form.cleaned_data['spk']
			profile.save()

			messages.success(request, _('Your Daftar PERT has been save successfully.'))
			return HttpResponseRedirect('/')
		else:
			messages.warning(request, form.errors)

	else:
		form = Proyek_Form()
		# form = Proyek_ModelForm()

	context = {
		'page_title': page_title,
		'estimasi_biaya': estimasi_biaya,
		'form': form,
		# 'total_estimasi_waktu': total_estimasi_waktu,
	}

	return render(request,'kegiatan/tabel_estimasi_biaya.html', context)


#@login_required()
def estimasi_biaya(request):
	page_title = _('Schedule')
	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_biaya = Schedule.objects.filter()

	if request.method == 'POST':
		form = EstimasiBiaya_ModelForm(request.POST or None)
		# formB = Kegiatan_ModelForm(request.POST or None)

		if form.is_valid():
			estimasi = form.save(commit=False)
			estimasi.kegiatan = form.cleaned_data['kegiatan']
			estimasi.estimasi_biaya = form.cleaned_data['estimasi_biaya']
			estimasi.save()

		# if formB.is_valid():
		#     kegiatan = formB.save(commit=False)
		#     kegiatan.kegiatan = formB.cleaned_data['kegiatan']
		#     kegiatan.estimasi_biaya = formB.cleaned_data['estimasi_biaya']
		#     kegiatan.save()

			messages.success(request, _('Your Schedule has been save successfully.'))
			return redirect('kegiatan:tabel_estimasi_biaya')
		else:
			messages.warning(request, form.errors)

	else:
		form = EstimasiBiaya_ModelForm(instance=request.user)
		# formB = Kegiatan_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
		'data_biaya': data_biaya,
	}

	return render(request,'kegiatan/estimasi_biaya.html', context)


def tabel_schedule(request):
	page_title = _('Tabel Time Schedule')
	schedule_data =   Schedule.objects.all()

	sum_cpi = Schedule.objects.aggregate(Sum('cost_performance_index'))
	sum_cpi = list(sum_cpi.values())
	sum_cpi = sum_cpi[0]

	obj_data =   Schedule.objects.all().values_list("cost_performance_index", flat=True).count()

	if sum_cpi is None:
		sum_cpi = 0
	else:
		sum_cpi = sum_cpi
		sum_cpi = sum_cpi/obj_data

	context = {
		'page_title': page_title,
		'schedule_data': schedule_data,
		'sum_cpi': sum_cpi,
	}

	return render(request,'kegiatan/tabel_schedule.html', context)
	# return redirect('kegiatan:tabel_schedule')


def tambah_schedule(request):
	page_title = _('Tambah Schedule')

	data_rab = Proyek.objects.all().values_list("rab", flat=True)
	data_rab = data_rab[0]
	data_rab = float(data_rab)

	if request.method == 'POST':
		form = Schedule_ModelForm(request.POST or None)

		if form.is_valid():
			# estimasi = Schedule()
			estimasi = form.save(commit=False)
			estimasi.minggu = form.cleaned_data['minggu']
			estimasi.progress_rencana = form.cleaned_data['progress_rencana']
			estimasi.progress_aktual = form.cleaned_data['progress_aktual']
			hitung_bcws = (estimasi.progress_rencana/99.0)*data_rab
			estimasi.bcws = hitung_bcws
			hitung_bcwp = (estimasi.progress_aktual/100.0)*data_rab
			estimasi.bcwp = hitung_bcwp
			estimasi.acwp = form.cleaned_data['acwp']
			hitung_acwp = estimasi.acwp
			hitung_cv = hitung_bcwp - hitung_acwp
			estimasi.cost_variance = hitung_cv
			hitung_cpi = hitung_bcwp / hitung_acwp
			estimasi.cost_performance_index = hitung_cpi
			estimasi.save()

			messages.success(request, _('Your Schedule has been save successfully.'))
			return redirect('kegiatan:tabel_schedule')
		else:
			messages.warning(request, form.errors)

	else:
		form = Schedule_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
	}

	return render(request,'kegiatan/tambah_schedule.html', context)


