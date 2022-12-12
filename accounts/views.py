from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .models import *
from proyek.models import *

# Create your views here.
def account_list(request):
    page_title = _('Proyek')
    data_user = UserProfile.objects.filter()

    context = {
        'page_title': page_title,
        'data_user': data_user,
    }
    return render(request,'account/account_list.html', context)


def account_profile(request, pk=None):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    page_title = _('SPK Proyeksi UMKT')
    user_id = request.user.is_authenticated
    user_data = UserProfile.objects.filter(id=user_id)

    print("user_data", user_data)

    context = {
        'page_title': page_title,
        'user_data': user_data,
    }
    return render(request, 'account/myprofile.html', context)
