from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .models import *
from user.models import *
from proyek.models import *

def data_list(request):
    page_title = _('Data')

    context = {
        'page_title': page_title,
    }
    return render(request,'data/data_list.html', context)

def kumpul_data(request):
    page_title = _('Data')
    data_user =   UserProfile.objects.all()
    data_proyek = Proyek.objects.filter()
    # data_proyek = get_object_or_404(Proyek, slug=category_slug)

    context = {
        'page_title': page_title,
    }
    return render(request,'data/data_list.html', context)

def analisa_data(request):
    page_title = _('Data')

    context = {
        'page_title': page_title,
    }
    return render(request,'data/data_list.html', context)
