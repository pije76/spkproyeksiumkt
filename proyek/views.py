from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


from .models import *
from .forms import *

from accounts.models import *

def daftar_proyek(request):
    page_title = _('Proyek')
    data_proyek = Proyek.objects.filter()

    context = {
        'page_title': page_title,
        'data_proyek': data_proyek,
    }
    return render(request,'proyek/daftar_proyek.html', context)

@login_required()
def tambah_proyek(request):
    page_title = _('Tambah Proyek')
    user_id = request.user.is_authenticated
    data_user = get_object_or_404(UserProfile, id=user_id)

    initial_value = {
        'user': data_user,
    }

    if request.method == 'POST':
        form = Proyek_Form(request.POST or None)

        if form.is_valid():
            proyek = Proyek()
            # proyek = form.save(commit=False)
            proyek.user = data_user
            proyek.nama_proyek = form.cleaned_data['nama_proyek']
            proyek.tanggal_mulai = form.cleaned_data['tanggal_mulai']
            proyek.tanggal_selesai = form.cleaned_data['tanggal_selesai']
            proyek.spk = form.cleaned_data['spk']
            proyek.save()

            messages.success(request, _('Your Proyek has been save successfully.'))
            return redirect('proyek:daftar_proyek')
        else:
            messages.warning(request, form.errors)

    else:
        form = Proyek_Form(initial=initial_value)
        # form = Proyek_ModelForm(instance=request.user, initial=initial_value)

    context = {
        'page_title': page_title,
        'form': form,
    }

    return render(request,'proyek/tambah_proyek.html', context)


