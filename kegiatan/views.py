from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.files import File
from django.db.models import Max, Sum, Count, Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *

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
#############################################################################
@login_required
def tabel_kegiatan(request):
	page_title = _('Daftar Kegiatan')
	data_user =   UserProfile.objects.all()
	data_kegiatan = Kegiatan.objects.filter()
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)
	# data_estimasi_waktu =   Estimasi_Waktu.objects.all()
	# item_biaya = Kegiatan.objects.values("biaya_kegiatan").annotate(Count("id")).count()
	total_bobot = Kegiatan.objects.aggregate(Sum('bobot_kegiatan'))
	total_biaya = Kegiatan.objects.aggregate(Sum('biaya_kegiatan'))
	total_duration = Kegiatan.objects.aggregate(Sum('duration'))
	varians_kegiatan = Kegiatan.objects.aggregate(Sum('varians_kegiatan'))
	# standar_varians_kejadian = np.sqrt(varians_kejadian)
	# standar_deviasi_kejadian = float(varians_kejadian)
	# standar_varians_kejadian = varians_kegiatan.values()
	standar_varians_kejadian = list(varians_kegiatan.values())
	standar_varians_kejadian = standar_varians_kejadian[0]
	# # standar_varians_kejadian = int(standar_varians_kejadian)
	standar_deviasi_kejadian = math.sqrt(standar_varians_kejadian)

	# print("standar_deviasi_kejadian", standar_deviasi_kejadian)


	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
		# 'data_estimasi_waktu': data_estimasi_waktu,
		'total_bobot': total_bobot,
		'total_biaya': total_biaya,
		'total_duration': total_duration,
		'varians_kegiatan': varians_kegiatan,
		'standar_deviasi_kejadian': standar_deviasi_kejadian,
	}

	return render(request,'kegiatan/tabel_kegiatan.html', context)

@login_required()
def tambah_kegiatan(request):
	page_title = _('Tambah Kegiatan')
	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_kegiatan = Kegiatan.objects.filter()
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)
	data_rab =   Kegiatan.objects.all().values_list("biaya_kegiatan")
	# name = Kegiatan.objects.all()[0]['biaya_kegiatan']

	if request.method == 'POST':
		# form = Kegiatan_Form(request.POST or None)
		form = Kegiatan_ModelForm(request.POST or None)

		if form.is_valid():
			# profile = Kegiatan()
			profile = form.save(commit=False)
			profile.proyek = form.cleaned_data['proyek']
			profile.nama_kegiatan = form.cleaned_data['nama_kegiatan']
			profile.kode = form.cleaned_data['kode']
			profile.predecessor = form.cleaned_data['predecessor']
			profile.hubungan_keterkaitan = form.cleaned_data['hubungan_keterkaitan']
			profile.bobot_kegiatan = form.cleaned_data['bobot_kegiatan']
			profile.biaya_kegiatan = form.cleaned_data['biaya_kegiatan']
			profile.save()

			# estimasi_rab = Proyek.objects.update_or_create(user=data_user, rab=biaya_kegiatan)


			messages.success(request, _('Your Kegiatan has been save successfully.'))
			return redirect('kegiatan:tabel_kegiatan')
		else:
			messages.warning(request, form.errors)

	else:
		# form = Kegiatan_Form()
		form = Kegiatan_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
		'form': form,
	}

	return render(request,'kegiatan/tambah_kegiatan.html', context)

#############################################################################
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

	rows = Kegiatan.objects.all().values_list('nama_kegiatan', 'kode', 'predecessor', 'duration', 'duration', 'duration', 'duration', 'duration', 'slack_time', 'critical')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	# wb.save(response)
	wb.save("/var/www/html/spkproyeksiumkt/upload/data.xlsx")
	# return response
	return redirect('kegiatan:tabel_estimasi_waktu')


############################### WAKTU ######################################
def hitungDurasi(a,m,b):
	return (a + (4*m) + b)/6

def hitungDeviasi(a,b):
	return (b-a)/6

def hitungVarians(a,b):
	return pow((b-a)/6,2)

def tabel_estimasi_waktu(request):
	page_title = _('Daftar Estimasi Waktu')
	data_user =   UserProfile.objects.all()
	estimasi_waktu = Estimasi_Waktu.objects.filter()
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)
	total_estimasi_waktu = Kegiatan.objects.aggregate(Sum('duration'))

	# estimasi_waktu_a = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_a", flat=True)[0]
	# estimasi_waktu_m = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_m", flat=True)[0]
	# estimasi_waktu_b = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_b", flat=True)[0]

	# estimasi_waktu_a = Estimasi_Waktu.objects.filter().aggregate(max_num=Max('estimasi_waktu_a'))
	# estimasi_waktu_m = Estimasi_Waktu.objects.filter().aggregate(max_num=Max('estimasi_waktu_m'))
	# estimasi_waktu_b = Estimasi_Waktu.objects.filter().aggregate(max_num=Max('estimasi_waktu_b'))

	# estimasi_waktu_a = estimasi_waktu_a.get('max_num', 3)
	# estimasi_waktu_m = estimasi_waktu_m.get('max_num', 3)
	# estimasi_waktu_b = estimasi_waktu_b.get('max_num', 3)

	estimasi_waktu_a = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_a")
	estimasi_waktu_m = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_m")
	estimasi_waktu_b = Estimasi_Waktu.objects.all().values_list("estimasi_waktu_b")

	estimasi_waktu_a = [item for item in estimasi_waktu_a]
	estimasi_waktu_m = [item for item in estimasi_waktu_m]
	estimasi_waktu_b = [item for item in estimasi_waktu_b]


	# durasi = hitungDurasi(estimasi_waktu_a, estimasi_waktu_m, estimasi_waktu_b)

	# print(estimasi_waktu_a)
	# print(type(estimasi_waktu_a))

	context = {
		'page_title': page_title,
		'estimasi_waktu': estimasi_waktu,
		'total_estimasi_waktu': total_estimasi_waktu,
		'estimasi_waktu_a': estimasi_waktu_a,
		'estimasi_waktu_m': estimasi_waktu_m,
		'estimasi_waktu_b': estimasi_waktu_b,
	}

	return render(request,'kegiatan/tabel_estimasi_waktu.html', context)


@login_required()
def estimasi_waktu(request):
	page_title = _('Estimasi Waktu')

	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_proyek =   Proyek.objects.filter(user=user_id)
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)

	data_rab = Kegiatan.objects.aggregate(Sum('biaya_kegiatan'))
	data_rab = list(data_rab.values())
	data_rab = data_rab[0]

	duration = Kegiatan.objects.aggregate(Sum('duration'))
	duration = list(duration.values())
	duration = duration[0]

	standar_deviasi = Kegiatan.objects.aggregate(Sum('standar_deviasi'))
	standar_deviasi = list(standar_deviasi.values())
	standar_deviasi = standar_deviasi[0]

	varians_kegiatan = Kegiatan.objects.aggregate(Sum('varians_kegiatan'))
	varians_kegiatan = list(varians_kegiatan.values())
	varians_kegiatan = varians_kegiatan[0]

	# standar_deviasi_kejadian = math.sqrt(standar_deviasi)

	# print("data_rab", data_rab)
	# print("duration", duration)
	# print("standar_deviasi", standar_deviasi)
	# print("standar_deviasi_kejadian", standar_deviasi_kejadian)
	# print("varians_kegiatan", varians_kegiatan)

	if request.method == 'POST':
		form = EstimasiWaktu_ModelForm(request.POST or None)

		if form.is_valid():
			estimasi = form.save(commit=False)

			estimasi.kegiatan = form.cleaned_data['kegiatan']
			estimasi.estimasi_waktu_a = form.cleaned_data['estimasi_waktu_a']
			estimasi.estimasi_waktu_m = form.cleaned_data['estimasi_waktu_m']
			estimasi.estimasi_waktu_b = form.cleaned_data['estimasi_waktu_b']
			hitung_Durasi = hitungDurasi(estimasi.estimasi_waktu_a, estimasi.estimasi_waktu_m, estimasi.estimasi_waktu_b)
			estimasi.duration = hitung_Durasi
			hitung_Deviasi = hitungDeviasi(estimasi.estimasi_waktu_a, estimasi.estimasi_waktu_b)
			estimasi.standar_deviasi = hitung_Deviasi
			hitung_Varians = hitungVarians(estimasi.estimasi_waktu_a, estimasi.estimasi_waktu_b)
			estimasi.varians_kegiatan = hitung_Varians
			estimasi.save()

			# obj, update = Estimasi_Waktu.objects.update_or_create(kegiatan=estimasi.kegiatan, estimasi_waktu_a=estimasi.estimasi_waktu_a, estimasi_waktu_m=estimasi.estimasi_waktu_m, estimasi_waktu_b=estimasi.estimasi_waktu_b)

			get_select = request.GET.get('get_select', None)
			get_select = estimasi.kegiatan.id
			set_kegiatan = Kegiatan.objects.get(id=get_select)
			set_kegiatan.duration = hitung_Durasi
			set_kegiatan.standar_deviasi = hitung_Deviasi
			set_kegiatan.varians_kegiatan = hitung_Varians

			column_header = ['Nama Kegiatan', 'Kode', 'Predecessor', 'Durasi', 'ES', 'EF', 'LS', 'LF', 'Slack', 'Lintasan', ]

			# for col_num in range(len(columns)):
			# 	ws.write(row_num, col_num, columns[col_num], font_style)

			row_kegiatan = Kegiatan.objects.all().values_list('nama_kegiatan', 'kode', 'predecessor', 'duration', 'earliest_start', 'earliest_finish', 'latest_start', 'latest_finish', 'slack_time', 'critical', named=True)
			# df.columns = column_header
			# data_cpm = pd.DataFrame(list(row_kegiatan))
			data_cpm = pd.DataFrame(list(row_kegiatan), columns=column_header)

			taskObject = []

			row_kegiatan = list(row_kegiatan)

			earlyStart = 0
			earliestFinish = 0
			successors = []
			latestStart = 0
			latest_finish = 0
			slack = 0
			critical = ''

			pred = []
			eF = []

			# if type(set_kegiatan.predecessor) is str:
			# 	ef = []
			# 	for j in set_kegiatan.predecessor:
			# 		for t in row_kegiatan:
			# 			if t.kode == j:
			# 				ef.append(t.earliest_finish)
			# 			set_kegiatan.earliest_start = max(ef)
			# 			set_kegiatan.save()
			# 			# set_kegiatan.save(update_fields=['earliest_start'])
			# 		del ef
			# 	else:
			# 		set_kegiatan.earliest_start = 0
			# 		set_kegiatan.save()
			# 		# set_kegiatan.save(update_fields=['earliest_start'])

			# 	set_kegiatan.earliest_finish = set_kegiatan.earliest_start + set_kegiatan.duration
			# 	set_kegiatan.save()
			# 	# set_kegiatan.save(update_fields=['earliest_finish'])

			set_kegiatan.save()

			# count_kegiatan = Kegiatan.objects.values("nama_kegiatan").annotate(Count("id"))
			# count_kegiatan = count_kegiatan.count()
			# count_kegiatan = count_kegiatan + 1

			# dataNode = []

			# for i in range(1, count_kegiatan):
			# 	dataNode.append([i, 0, 0])

			# print("count_kegiatan", count_kegiatan)

			messages.success(request, _('Your Estimasi Waktu has been save successfully.'))
			return redirect('kegiatan:tabel_estimasi_waktu')
		else:
			messages.warning(request, form.errors)

	else:
		form = EstimasiWaktu_ModelForm(instance=request.user)

	context = {
		'page_title': page_title,
		'form': form,
	}

	return render(request,'kegiatan/estimasi_waktu.html', context)


################################ CPM ##########################################


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
				item.earliest_start = max(ef)
				item.save(update_fields=['earliest_start'])
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
			item.latest_finish = max(eF)

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


			# print("eF", eF)
			# print("successors", successors)
			# print("row_kegiatan", row_kegiatan)

			# for item in row_kegiatan_list:
			for t in eF:
				# for t in eF:
				# print("item", item)
				# print("t", t)
					# item.latest_finish = t
					# item.save()
					# item.save(update_fields=['latest_finish'])
				row_kegiatan = Kegiatan.objects.exclude(latest_finish__isnull=False)
				# print("row_kegiatan", row_kegiatan)
				for item.latest_finish in row_kegiatan:
				# for item in varians_kejadian:
				# 	print(item['varians_kejadian'])

				# 	# Kegiatan.objects.exclude(latest_finish__isnull=False).update(latest_finish = t)
					item.latest_finish = t
					item.latest_start = item.latest_finish - item.duration
					print(item.latest_finish)
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
					# print("t", t)
					# print("t.latest_start", t.latest_start)
					# if t.kode == x:
					# 	# t.latest_start = 0
					# 	minLs.append(t.latest_start)
						# print("minLs", minLs)
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



def tabel_cpm(request):
	page_title = _('Tabel CPM')
	user_id = request.user.is_authenticated
	data_kegiatan = Kegiatan.objects.all()

	context = {
		'page_title': page_title,
		'data_kegiatan': data_kegiatan,
	}

	return render(request,'kegiatan/tabel_cpm.html', context)



################################ BIAYA ##########################################
def daftar_estimasi_biaya(request):
	page_title = _('Daftar Estimasi Biaya')
	data_user =   UserProfile.objects.all()
	estimasi_biaya = Estimasi_Biaya.objects.filter()
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)
	# total_estimasi_waktu = Estimasi_Waktu.objects.aggregate(Sum('duration'))


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

			messages.success(request, _('Your Daftar Estimasi Waktu has been save successfully.'))
			return HttpResponseRedirect('/')
		else:
			messages.warning(request, form.errors)

	else:
		form = Proyek_Form()
		# form = Proyek_ModelForm()
		# print("form", form)

	context = {
		'page_title': page_title,
		'estimasi_biaya': estimasi_biaya,
		'form': form,
		# 'total_estimasi_waktu': total_estimasi_waktu,
	}

	return render(request,'kegiatan/daftar_estimasi_biaya.html', context)



@login_required()
def estimasi_biaya(request):
	page_title = _('Estimasi Biaya')
	user_id = request.user.is_authenticated
	data_user =   UserProfile.objects.filter(id=user_id)
	data_biaya = Estimasi_Biaya.objects.filter()
	# data_proyek = get_object_or_404(Proyek, slug=category_slug)

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
			return redirect('kegiatan:daftar_estimasi_biaya')
		else:
			messages.warning(request, form.errors)

	else:
		form = EstimasiBiaya_ModelForm(instance=request.user)
		# formB = Kegiatan_ModelForm(instance=request.user)
		# print("form", form)
		# print("formB", formB)

	context = {
		'page_title': page_title,
		'form': form,
		'data_biaya': data_biaya,
	}

	return render(request,'kegiatan/estimasi_biaya.html', context)


