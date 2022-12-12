from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile

import string

test_list = []
test_list = list(string.ascii_uppercase)

ALPHABETS_CHOICES = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C')
)

# Create your models here.
class Proyek(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    nama_proyek = models.CharField(_("Nama Proyek"), max_length=255, blank=True, null=True)
    tanggal_mulai = models.DateField(_("Tanggal Mulai"), blank=True, null=True)
    tanggal_selesai = models.DateField(_("Tanggal Mulai"), blank=True, null=True)
    spk = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('nama_proyek',)
        verbose_name = 'Proyek'
        verbose_name_plural = 'Proyek'

    def __str__(self):
    #     return str(self.id)
        return self.nama_proyek

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.expired = self.created + datetime.timedelta(days=30)
    #         super().save(*args, **kwargs)

    @property
    def total_hari(self):
        return (self.tanggal_selesai - self.tanggal_mulai).days

