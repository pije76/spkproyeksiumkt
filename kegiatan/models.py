from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile
from proyek.models import Proyek
from .choices import *

import os
import uuid


# Create your models here.
class Kegiatan(models.Model):
	# user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
	proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
	nama_kegiatan = models.CharField(_("Nama Kegiatan"), max_length=255, blank=False, null=True)
	kode = models.CharField(max_length=255, choices=KODE_CHOICES, default="-", blank=True, null=True)
	bobot_kegiatan = models.DecimalField(_("Bobot Kegiatan"), max_digits=3, decimal_places=2, blank=True, null=True)
	biaya_kegiatan = models.DecimalField(_("Biaya Kegiatan"), max_digits=10, decimal_places=0, blank=True, null=True)
	predecessor = models.CharField(max_length=255, choices=PREDECESSOR_CHOICES, default="-", blank=True, null=True)
	hubungan_keterkaitan = models.CharField(max_length=255, choices=KONSTRAIN_CHOICES, default="ss", null=True, blank=True)
	duration = models.FloatField(blank=True, null=True)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Kegiatan'
		verbose_name_plural = 'Kegiatan'

	def __str__(self):
	#     return str(self.id)
		# return self.nama_kegiatan
		# return self.kode
		return str(self.nama_kegiatan)
		# return f"{self.kode} - {self.nama_kegiatan}"


class PERT(models.Model):
	kegiatan = models.OneToOneField(Kegiatan, on_delete=models.CASCADE, blank=False, null=True)
	duration = models.FloatField(blank=True, null=True)
	optimistic_time = models.FloatField(_("Optimistic Time"), blank=True, null=True)
	most_likely_time = models.FloatField(_("Most Likely Time"), blank=True, null=True)
	pessimistic_time = models.FloatField(_("Pessimistic Time"), blank=True, null=True)
	standar_deviasi = models.FloatField(_("Standar Deviasi"), blank=True, null=True)
	varians_kegiatan = models.FloatField(_("Varians Kegiatan"), blank=True, null=True)


	class Meta:
		ordering = ('id',)
		verbose_name = 'PERT'
		verbose_name_plural = 'PERT'

	def __str__(self):
		return str(self.id)


class CPM(models.Model):
	kegiatan = models.CharField(max_length=255, blank=True, null=True)
	kode = models.CharField(max_length=255, choices=KODE_CHOICES, default="-", blank=True, null=True)
	duration = models.FloatField(blank=True, null=True)
	predecessor = models.CharField(max_length=255, choices=PREDECESSOR_CHOICES, default="-", blank=True, null=True)
	earliest_start = models.FloatField(_("ES"), blank=True, null=True)
	earliest_finish = models.FloatField(_("EF"), blank=True, null=True)
	latest_start = models.FloatField(_("LS"), blank=True, null=True)
	latest_finish = models.FloatField(_("LF"), blank=True, null=True)
	slack_time = models.FloatField(_("Slack"), blank=True, null=True)
	critical = models.CharField(max_length=255, blank=True, null=True)
	successors = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		ordering = ('id',)
		verbose_name = 'CPM'
		verbose_name_plural = 'CPM'

	# def __str__(self):
	#     return str(self.id)
		# return self.nama_kegiatan
		# return self.kode
		# return str(self.nama_kegiatan)
		# return f"{self.kode} - {self.nama_kegiatan}"


class Estimasi_Biaya(models.Model):
	minggu = models.IntegerField(_("Minggu"), blank=True, null=True)
	progress_rencana = models.FloatField(_("Progress Rencana"), blank=True, null=True)
	progress_aktual = models.FloatField(_("Progress Aktual"), blank=True, null=True)
	acwp = models.DecimalField(_("Actual Cost of Work Planned"), max_digits=10, decimal_places=2, blank=True, null=True)
	bcwp = models.DecimalField(_("Budgeted Cost of Work Planned "), max_digits=10, decimal_places=2, blank=True, null=True)
	bcws = models.DecimalField(_("Budgeted Cost of Work Schedule"), max_digits=10, decimal_places=2, blank=True, null=True)
	cost_variance = models.DecimalField(_("Cost Variance"), max_digits=10, decimal_places=2, blank=True, null=True)
	cost_performance_index = models.FloatField(_("Cost Performance Index"), blank=True, null=True)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Estimasi Biaya'
		verbose_name_plural = 'Estimasi Biaya'

	# def __str__(self):
	#     return str(self.id)

	# @property
	# def price_display(self):
	#     return "Rp%s" % self.estimasi_biaya
