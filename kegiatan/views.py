from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import *
from .forms import *
from proyek.forms import *

from accounts.models import *

# Create your views here.
def daftar_kegiatan(request):
    page_title = _('Daftar Kegiatan')
    data_user =   UserProfile.objects.all()
    data_kegiatan = Kegiatan.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

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

            messages.success(request, _('Your profile has been change successfully.'))
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)

    else:
        form = Proyek_Form()
        # form = Proyek_ModelForm()
        print("form", form)

    context = {
        'page_title': page_title,
        'data_kegiatan': data_kegiatan,
        'form': form,
    }

    return render(request,'kegiatan/daftar_kegiatan.html', context)

@login_required()
def tambah_kegiatan(request):
    page_title = _('Tambah Proyek')
    data_user =   UserProfile.objects.all()
    data_kegiatan = Kegiatan.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

    if request.method == 'POST':
        # form = Kegiatan_Form(request.POST or None)
        form = Kegiatan_ModelForm(request.POST or None)

        if form.is_valid():
            # profile = Kegiatan()
            profile = form.save(commit=False)
            profile.proyek = form.cleaned_data['proyek']
            profile.nama_kegiatan = form.cleaned_data['nama_kegiatan']
            profile.kode = form.cleaned_data['kode']
            profile.save()

            messages.success(request, _('Your profile has been change successfully.'))
            return redirect('kegiatan:daftar_kegiatan')
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


def standar_deviasi_kegiatan(request):
    page_title = _('Standar Deviasi Kegiatan')
    data_user =   UserProfile.objects.all()
    data_kegiatan = Estimasi_Waktu.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

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

            messages.success(request, _('Your profile has been change successfully.'))
            return redirect('kegiatan:standar_deviasi_kegiatan')
        else:
            messages.warning(request, form.errors)

    else:
        form = Proyek_Form()
        # form = Proyek_ModelForm()
        print("form", form)

    context = {
        'page_title': page_title,
        'data_kegiatan': data_kegiatan,
        'form': form,
    }

    return render(request,'kegiatan/standar_deviasi_kegiatan.html', context)


def varians_kegiatan(request):
    page_title = _('Varians Kegiatan')
    data_user =   UserProfile.objects.all()
    data_kegiatan = Estimasi_Waktu.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

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

            messages.success(request, _('Your profile has been change successfully.'))
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)

    else:
        form = Proyek_Form()
        # form = Proyek_ModelForm()

    context = {
        'page_title': page_title,
        'data_kegiatan': data_kegiatan,
        'form': form,
    }

    return render(request,'kegiatan/varians_kegiatan.html', context)


################################################################################3333
def daftar_estimasi_waktu(request):
    page_title = _('Daftar Estimasi Waktu')
    data_user =   UserProfile.objects.all()
    estimasi_waktu = Estimasi_Waktu.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)
    total_estimasi_waktu = Estimasi_Waktu.objects.aggregate(Sum('expected_duration'))


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
        'estimasi_waktu': estimasi_waktu,
        'form': form,
        'total_estimasi_waktu': total_estimasi_waktu,
    }

    return render(request,'kegiatan/daftar_estimasi_waktu.html', context)


@login_required()
def estimasi_waktu(request):
    page_title = _('Estimasi Waktu')
    data_user =   UserProfile.objects.all()
    data_proyek = Proyek.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

    if request.method == 'POST':
        form = EstimasiWaktu_ModelForm(request.POST or None)

        if form.is_valid():
            estimasi = form.save(commit=False)
            estimasi.kegiatan = form.cleaned_data['kegiatan']
            estimasi.estimasi_waktu_a = form.cleaned_data['estimasi_waktu_a']
            estimasi.estimasi_waktu_m = form.cleaned_data['estimasi_waktu_m']
            estimasi.estimasi_waktu_b = form.cleaned_data['estimasi_waktu_b']
            estimasi.expected_duration = (estimasi.estimasi_waktu_a + (estimasi.estimasi_waktu_m*4.0) + estimasi.estimasi_waktu_b)/6.0
            estimasi.expected_duration = estimasi.expected_duration
            estimasi.standar_deviasi = (estimasi.estimasi_waktu_b - estimasi.estimasi_waktu_a)/6.0
            estimasi.standar_deviasi = estimasi.standar_deviasi
            estimasi.varians_kegiatan = estimasi.standar_deviasi * estimasi.standar_deviasi
            estimasi.save()

            messages.success(request, _('Your Estimasi Waktu has been save successfully.'))
            return redirect('kegiatan:daftar_estimasi_waktu')
        else:
            messages.warning(request, form.errors)

    else:
        form = EstimasiWaktu_ModelForm()
        print("form", form)

    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request,'kegiatan/estimasi_waktu.html', context)


def critical_path(request):
    page_title = _('Estimasi Waktu')
    data_user =   UserProfile.objects.all()
    data_proyek = Proyek.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

    if request.method == 'POST':
        form = EstimasiWaktu_ModelForm(request.POST or None)

        if form.is_valid():
            estimasi = form.save(commit=False)
            estimasi.kegiatan = form.cleaned_data['kegiatan']
            estimasi.estimasi_waktu_a = form.cleaned_data['estimasi_waktu_a']
            estimasi.estimasi_waktu_m = form.cleaned_data['estimasi_waktu_m']
            estimasi.estimasi_waktu_b = form.cleaned_data['estimasi_waktu_b']
            estimasi.expected_duration = (estimasi.estimasi_waktu_a + (estimasi.estimasi_waktu_m*4.0) + estimasi.estimasi_waktu_b)/6.0
            estimasi.expected_duration = estimasi.expected_duration
            estimasi.standar_deviasi = (estimasi.estimasi_waktu_b - estimasi.estimasi_waktu_a)/6.0
            estimasi.standar_deviasi = estimasi.standar_deviasi
            estimasi.varians_kegiatan = estimasi.standar_deviasi * estimasi.standar_deviasi
            estimasi.save()

            messages.success(request, _('Your Estimasi Waktu has been save successfully.'))
            return redirect('kegiatan:daftar_estimasi_waktu')
        else:
            messages.warning(request, form.errors)

    else:
        form = EstimasiWaktu_ModelForm()
        print("form", form)

    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request,'kegiatan/critical_path.html', context)



#################################################################################
def daftar_estimasi_biaya(request):
    page_title = _('Daftar Estimasi Biaya')
    data_user =   UserProfile.objects.all()
    estimasi_biaya = Estimasi_Biaya.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)
    # total_estimasi_waktu = Estimasi_Waktu.objects.aggregate(Sum('expected_duration'))


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
    data_proyek = Proyek.objects.filter()
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
        # 'formB': formB,
    }

    return render(request,'kegiatan/estimasi_biaya.html', context)


