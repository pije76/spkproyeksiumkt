from django.db import models
from django.utils.translation import gettext_lazy as _

# from user.models import UserProfile

KONSTRAIN_CHOICES = (
    ('ss', 'Start to Start'),
    ('fs', 'Finish to Start')
)

ESTIMATE_CHOICES = (
    ('a', 'Most Likely Time'),
    ('m', 'Optimistic Time'),
    ('b', 'Pessismistic Time')
)

# Create your models here.
class Proyek(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    nama_proyek = models.CharField(_("Nama Proyek"), max_length=30, blank=True, null=True)
    SPK = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        ordering = ('nama_proyek',)
        verbose_name = 'Proyek'
        verbose_name_plural = 'Proyek'

    def __str__(self):
        return str(self.id)


class Estimasi_Waktu(models.Model):
    # proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
    kode = models.CharField(max_length=255, blank=True, null=True)
    perkiraan_waktu = models.IntegerField()

    class Meta:
        ordering = ('kode',)
        verbose_name = 'Estimasi Waktu'
        verbose_name_plural = 'Estimasi Waktu'

    def __str__(self):
        return str(self.id)


class PERT(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    kode = models.CharField(max_length=255, blank=True, null=True)
    jenis_kegiatan = models.CharField(max_length=255, blank=True, null=True)
    predecessor = models.CharField(max_length=255, blank=True, null=True)
    hubungan_keterkaitan = models.CharField(max_length=255, choices=KONSTRAIN_CHOICES, default="ss", null=True, blank=True)
    perkiraan_waktu = models.ForeignKey(Estimasi_Waktu, on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        ordering = ('kode',)
        verbose_name = 'PERT'
        verbose_name_plural = 'PERT'

    def __str__(self):
        return str(self.id)

