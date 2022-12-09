from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import *

# Create your models here.
class Proyek(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    nama_proyek = models.CharField(_("Nama Proyek"), max_length=255, blank=True, null=True)
    SPK = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('nama_proyek',)
        verbose_name = 'Proyek'
        verbose_name_plural = 'Proyek'

    def __str__(self):
        return str(self.nama_proyek)

