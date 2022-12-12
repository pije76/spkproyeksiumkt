from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile
from proyek.models import Proyek


KONSTRAIN_CHOICES = (
    ('-', '-'),
    ('S-S', 'Start to Start'),
    ('F-S', 'Finish to Start'),
    ('F-F', 'Finish to Finish')
)

ESTIMATE_CHOICES = (
    ('a', 'Most Likely Time'),
    ('m', 'Optimistic Time'),
    ('b', 'Pessismistic Time')
)


# Create your models here.
class Kegiatan(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
    nama_kegiatan = models.CharField(_("Nama Kegiatan"), max_length=255, blank=True, null=True)
    kode = models.CharField(max_length=255, blank=True, null=True)
    predecessor = models.CharField(max_length=255, blank=True, null=True)
    hubungan_keterkaitan = models.CharField(max_length=255, choices=KONSTRAIN_CHOICES, default="ss", null=True, blank=True)
    bobot_kegiatan = models.DecimalField(_("Bobot Kegiatan"), max_digits=5, decimal_places=1, blank=True, null=True)
    # estimasi_biaya = models.ForeignKey(Estimasi_Biaya, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_biaya_kegiatan')
    # estimasi_waktu = models.ForeignKey(Estimasi_Waktu, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_waktu_kegiatan')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Kegiatan'
        verbose_name_plural = 'Kegiatan'

    def __str__(self):
    #     return str(self.id)
        # return self.nama_kegiatan
        # return self.kode
        # return str(self.nama_kegiatan)
        return f"{self.kode} - {self.nama_kegiatan}"
        # return f"{self.id}-{self.title}-{self.status}"


class Estimasi_Waktu(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, blank=False, null=True)
    # kode = models.CharField(max_length=255, blank=True, null=True)
    # tipe_estimasi = models.CharField(_("Tipe Estimasi"), max_length=255, choices=ESTIMATE_CHOICES, default="a", null=True, blank=True)
    # estimasi_waktu = models.IntegerField(_("Estimasi Waktu"))
    estimasi_waktu_a = models.FloatField(_("Optimistic Time"), blank=True, null=True)
    estimasi_waktu_m = models.FloatField(_("Most Likely Time"), blank=True, null=True)
    estimasi_waktu_b = models.FloatField(_("Pessismistic Time"), blank=True, null=True)
    expected_duration = models.FloatField(_("Expected Duration"), blank=True, null=True)
    standar_deviasi = models.FloatField(_("Standar Deviasi"), blank=True, null=True)
    varians_kegiatan = models.FloatField(_("Varians Kegiatan"), blank=True, null=True)


    class Meta:
        ordering = ('kegiatan',)
        verbose_name = 'Estimasi Waktu'
        verbose_name_plural = 'Estimasi Waktu'

    # def __str__(self):
    #     return str(self.id)


class Estimasi_Biaya(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, blank=False, null=True)
    # kode = models.CharField(max_length=255, blank=True, null=True)
    # estimasi_biaya = models.IntegerField(_("Perkiraan Biaya"))
    estimasi_biaya = models.DecimalField(_("Perkiraan Biaya"), max_digits=10, decimal_places=0)
    # estimasi_biaya = MoneyField(max_digits=10, decimal_places=0, default_currency='IDR')

    class Meta:
        ordering = ('kegiatan',)
        verbose_name = 'Estimasi Biaya'
        verbose_name_plural = 'Estimasi Biaya'

    # def __str__(self):
    #     return str(self.id)

    # @property
    # def price_display(self):
    #     return "Rp%s" % self.estimasi_biaya
