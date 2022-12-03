from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from proyek.models import *

# Create your views here.
def index(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    page_title = _('Check the Best Blood Test &amp; Pathology Lab in India with Shrinivas Diagnostics Labs')
    user_id = request.user.is_authenticated
    proyek = Proyek.objects.filter(user=user_id)

    context = {
        'page_title': page_title,
        'proyek': proyek,
    }
    return render(request, 'homepage/home.html', context)
