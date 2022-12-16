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
	estimasi_waktu = PERT.objects.filter()
	total_estimasi_waktu = PERT.objects.aggregate(Sum('duration'))
	total_duration = PERT.objects.aggregate(Sum('duration'))
	varians_kegiatan = PERT.objects.aggregate(Sum('varians_kegiatan'))

	optimistic_time = PERT.objects.all().values_list("optimistic_time")
	most_likely_time = PERT.objects.all().values_list("most_likely_time")
	pessimistic_time = PERT.objects.all().values_list("pessimistic_time")

	optimistic_time = [item for item in optimistic_time]
	most_likely_time = [item for item in most_likely_time]
	pessimistic_time = [item for item in pessimistic_time]

	context = {
		'page_title': page_title,
		'estimasi_waktu': estimasi_waktu,
		'total_estimasi_waktu': total_estimasi_waktu,
		'optimistic_time': optimistic_time,
		'most_likely_time': most_likely_time,
		'pessimistic_time': pessimistic_time,
		'total_duration': total_duration,
		'varians_kegiatan': varians_kegiatan,
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
			# print("get_select POST", get_select)
			# get_select = estimasi.kegiatan.id
			# print("get_select", get_select)
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
def readData():
	PATH = "/var/www/html/spkproyeksiumkt/upload/"
	os.chdir(PATH)

	df = pd.read_csv('data.xlsx')
	sheet = pd.read_excel(df, sheet_name='Sheet1')
	return(sheet)


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


def create_forwardsCPM(request):
	page_title = _('Create CPM')
	row_kegiatan = Kegiatan.objects.all()
	row_kegiatan_list = list(row_kegiatan)

	for item in row_kegiatan_list:
		if type(item.predecessor) is str:
			item.predecessor = item.predecessor.upper()
			ef = []

			for j in item.predecessor:
				for t in row_kegiatan_list:
					if t.kode == j:
						ef.append(t.earliest_finish)
				item.earliest_start = max(ef, default=0)
				item.save(update_fields=['earliest_start'])

				item.earliest_finish = item.earliest_start + item.duration
				item.save(update_fields=['earliest_finish'])

			del ef
		else:
			item.earliest_start = 0
			item.save(update_fields=['earliest_start'])

			item.earliest_finish = item.earliest_start + item.duration
			item.save(update_fields=['earliest_finish'])

	context = {
		'page_title': page_title,
		'row_kegiatan': row_kegiatan,
	}

	# return render(request,'kegiatan/tabel_cpm.html', context)
	return redirect('kegiatan:tabel_cpm')


def create_backwardsCPM(request):
	# RULE1: LATEST FINISH OF THE ACTIVITY WHICH IS NOT A PREDECESSOR OF ANY ACTIVITY IS THE MAXIMUM EARLIEST FINISH
	# RULE2: LATEST FINISH OF THE ACTIVITY WHICH IS A PREDECESSOR OF ANY ACTIVITY IS THE MINIMUM EARLIEST FINISH OF ITS SUCESSORS
	# RULE3: THE LATEST START OF THE ACITVITY OF THE ACTIVITY IS LATEST FINISH LESS THE ACTIVITY TIME
	page_title = _('Create CPM')
	row_kegiatan = Kegiatan.objects.all()
	row_kegiatan_list = list(row_kegiatan)
	queryset = reversed(Kegiatan.objects.all())
	row_kegiatan_list_reversed = list(queryset)

	pred = []
	eF = []
	successors = []
	latest_start = 0
	latest_finish = 0

	# THIS FOR LOOP WILL GATHER EARLIEST FINISH OF ALL TASKS AND FILL THE PREDECESSORS LIST OF ALL THE TASKS
	for item in row_kegiatan_list:
		if type(item.predecessor) is str:
			for j in item.predecessor:
				pattern = re.compile(r'[A-Z]')
				match = pattern.finditer(j)

				for r in match:
					pred.append(j) # FILL IN PREDECCSOR LIST OF ALL TASKS
				# FILL IN SUCCESSORS
				for m in row_kegiatan_list:
					if m.kode == j:
						successors.append(item.kode)
		eF.append(item.earliest_finish)

	for item in row_kegiatan_list_reversed:

		if item.kode not in pred:
			item.latest_finish = max(eF, default=0)

			item.save(update_fields=['latest_finish'])
			eF.remove(max(eF))
			item.latest_start = item.latest_finish - item.duration
			item.save(update_fields=['latest_start'])
			item.slack_time = item.latest_finish - item.earliest_finish
			item.save(update_fields=['slack_time'])
			if item.slack_time > 0:
				item.critical = '-'
				item.save(update_fields=['critical'])
			else:
				item.critical = 'Kritis'
				item.save(update_fields=['critical'])
		else:
			# for k in eF:
			# 	item.latest_finish = k
			# 	item.save(update_fields=['latest_start'])

			minLs = []
			successors = list(reversed(successors))
			# row_kegiatan = reversed(Kegiatan.objects.filter().exclude(latest_finish__in=max(eF)))
			# row_kegiatan = reversed(Kegiatan.objects.filter(~Q(latest_finish__in=eF)))
			# row_kegiatan = reversed(Kegiatan.objects.filter().values_list("latest_finish", flat=True))
			# row_kegiatan = Kegiatan.objects.exclude(latest_finish__isnull=False).values_list("kode", flat=True)
			row_kegiatan = Kegiatan.objects.exclude(latest_finish__isnull=False)
			row_kegiatan = list(reversed(row_kegiatan))
			# row_kegiatan_list = list(row_kegiatan)



			# for item in row_kegiatan_list:
			for t in eF:
				# for t in eF:
					# item.latest_finish = t
					# item.save()
					# item.save(update_fields=['latest_finish'])
				row_kegiatan = Kegiatan.objects.exclude(latest_finish__isnull=False)
				for item.latest_finish in row_kegiatan:
				# for item in varians_kejadian:

				# 	# Kegiatan.objects.exclude(latest_finish__isnull=False).update(latest_finish = t)
					item.latest_finish = t
					item.latest_start = item.latest_finish - item.duration
					# item.save()
					# item.update(latest_finish=t) # GAGAL
					item.save(update_fields=['latest_finish'])
					item.save(update_fields=['latest_start'])
					item.slack_time = item.latest_finish - item.earliest_finish
					item.save(update_fields=['slack_time'])
					if item.slack_time > 0:
						item.critical = '-'
						item.save(update_fields=['critical'])
					else:
						item.critical = 'Kritis'
						item.save(update_fields=['critical'])
				# 	# item.save(latest_finish = t)
				# 	item.latest_start = item.latest_finish - item.duration
				# 	item.save(update_fields=['latest_start'])

			# for x in successors:
			# 	for t in (row_kegiatan_list):
					# if t.kode == x:
					# 	# t.latest_start = 0
					# 	minLs.append(t.latest_start)
			# item.latest_finish = min(minLs)
			# item.save(update_fields=['latest_finish'])
			# del minLs

			# item.latest_start = item.latest_finish - item.duration
			# item.save(update_fields=['latest_start'])

	context = {
		'page_title': page_title,
		'row_kegiatan': row_kegiatan,
	}

	# return render(request,'kegiatan/tabel_cpm.html', context)
	return redirect('kegiatan:tabel_cpm')


################################ SCHEDULE & BIAYA ##########################################
def tabel_estimasi_biaya(request):
	page_title = _('Daftar Estimasi Biaya')
	data_user =   UserProfile.objects.all()
	estimasi_biaya = Estimasi_Biaya.objects.filter()
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
	page_title = _('Estimasi Biaya')
	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_biaya = Estimasi_Biaya.objects.filter()

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

			messages.success(request, _('Your Estimasi Biaya has been save successfully.'))
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
	schedule_data =   Estimasi_Biaya.objects.all()

	context = {
		'page_title': page_title,
		'schedule_data': schedule_data,
	}

	return render(request,'kegiatan/tabel_schedule.html', context)
	# return redirect('kegiatan:tabel_schedule')


def tambah_schedule(request):
	page_title = _('Tambah Schedule')


	if request.method == 'POST':
		form = Schedule_ModelForm(request.POST or None)

		if form.is_valid():
			# estimasi = Schedule_ModelForm()
			estimasi = form.save(commit=False)
			estimasi.kegiatan = form.cleaned_data['kegiatan']
			estimasi.minggu = form.cleaned_data['minggu']
			estimasi.progress_rencana = form.cleaned_data['progress_rencana']
			estimasi.progress_aktual = form.cleaned_data['progress_aktual']
			estimasi.save()

			messages.success(request, _('Your Schedulehas been save successfully.'))
			return redirect('kegiatan:tabel_schedule')
		else:
			messages.warning(request, form.errors)

	else:
		form = Schedule_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
		# 'data_biaya': data_biaya,
	}

	return render(request,'kegiatan/tambah_schedule.html', context)


