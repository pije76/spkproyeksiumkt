from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .models import *


def data_list(request):
    page_title = _('Data')

    context = {
        'page_title': page_title,
    }
    return render(request,'data/data_list.html', context)
