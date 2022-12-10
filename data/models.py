from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import *
from proyek.models import *

# Create your models here.
class Data(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
    # nama_data = models.CharField(_("Nama Data"), max_length=255, blank=True, null=True)
    # waktu = models.DateTimeField(auto_now_add=False)
    waktu = models.CharField(_("Waktu"), max_length=20, blank=True, null=True)
    # biaya = models.DecimalField(max_digits=100, decimal_places=2)
    biaya = models.CharField(_("Biaya"), max_length=30, blank=True, null=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Data'
        verbose_name_plural = 'Data'

    def __str__(self):
        return str(self.nama_data)

