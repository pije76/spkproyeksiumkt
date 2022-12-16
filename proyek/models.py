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
    spk = models.CharField(max_length=255, blank=True, null=True)
    rab = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ('nama_proyek',)
        verbose_name = 'Proyek'
        verbose_name_plural = 'Proyek'

    def __str__(self):
        return self.nama_proyek

