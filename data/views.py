from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *

from accounts.models import *
from proyek.models import *

def daftar_data(request):
    page_title = _('Data')
    data_proyek = Data.objects.filter()

    context = {
        'page_title': page_title,
        'data_proyek': data_proyek,
    }
    return render(request,'data/daftar_data.html', context)

def tambah_data(request):
    page_title = _('Tambah Data')
    data_user =   UserProfile.objects.all()
    data_proyek = Proyek.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

    if request.method == 'POST':
        # form = Data_Form(request.POST or None)
        form = Data_ModelForm(request.POST or None)

        if form.is_valid():
            # profile = Data()
            profile = form.save(commit=False)
            profile.user = form.cleaned_data['user']
            profile.proyek = form.cleaned_data['proyek']
            profile.waktu = form.cleaned_data['waktu']
            profile.save()

            messages.success(request, _('Your profile has been change successfully.'))
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)

    else:
        # form = Data_Form()
        form = Data_ModelForm()

    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request,'data/tambah_data.html', context)


def analisa_data(request):
    page_title = _('Data')

    context = {
        'page_title': page_title,
    }
    return render(request,'data/data_list.html', context)