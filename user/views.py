from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from proyek.models import *

# Create your views here.
def account_profile(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    page_title = _('SPK Proyeksi UMKT')
    user_id = request.user.is_authenticated
    proyek = Proyek.objects.filter(user=user_id)

    context = {
        'page_title': page_title,
        'proyek': proyek,
    }
    return render(request, 'homepage/home.html', context)
