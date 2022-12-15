from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile
from proyek.models import Proyek

import os
import uuid

KONSTRAIN_CHOICES = (
	('', '-'),
	('S-S', 'Start to Start'),
	('F-S', 'Finish to Start'),
	('F-F', 'Finish to Finish')
)

ESTIMATE_CHOICES = (
	('a', 'Most Likely Time'),
	('m', 'Optimistic Time'),
	('b', 'Pessismistic Time')
)


def user_directory_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
	return os.path.join("files", filename)
	# return os.path.join('members/forecast/', format(instance.username), filename)
	# return os.path.join('members/', f'{self.name}{self.type}Chart.svg')
	# set_upload_dir = 'members/{0}/forecast/{1}'.format(instance.username, filename)
	return 'members/{0}/forecast/{1}'.format(instance.username, filename)
	# return 'members'
	# return set_upload_dir
	# cache.set('set_upload_dir', set_upload_dir)
	# return os.path.join('members/', f'{type}')
	# cv2.imwrite(os.path.join(upload_to(),'new_image'+str(i)+'.jpg'),frame)
	# field.upload_to = f'{self.company.name}/{str(date.today())}


# Create your models here.
class Kegiatan(models.Model):
	# user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
	proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=False, null=True)
	nama_kegiatan = models.CharField(_("Nama Kegiatan"), max_length=255, blank=False, null=True)
	kode = models.CharField(max_length=255, blank=True, null=True)
	predecessor = models.CharField(max_length=255, blank=True, null=True)
	hubungan_keterkaitan = models.CharField(max_length=255, choices=KONSTRAIN_CHOICES, default="ss", null=True, blank=True)
	bobot_kegiatan = models.DecimalField(_("Bobot Kegiatan"), max_digits=5, decimal_places=1, blank=True, null=True)
	biaya_kegiatan = models.DecimalField(_("Biaya Kegiatan"), max_digits=10, decimal_places=0, blank=True, null=True)
	# estimasi_biaya = models.ForeignKey(Estimasi_Biaya, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_biaya_kegiatan')
	# estimasi_waktu = models.ForeignKey(Estimasi_Waktu, on_delete=models.CASCADE, blank=False, null=True, related_name='estimasi_waktu_kegiatan')
	duration = models.FloatField(blank=True, null=True)
	standar_deviasi = models.FloatField(_("Standar Deviasi"), blank=True, null=True)
	varians_kegiatan = models.FloatField(_("Varians Kegiatan"), blank=True, null=True)
	earliest_start = models.FloatField(_("ES"), blank=True, null=True)
	earliest_finish = models.FloatField(_("EF"), blank=True, null=True)
	latest_start = models.FloatField(_("LS"), blank=True, null=True)
	latest_finish = models.FloatField(_("LF"), blank=True, null=True)
	slack_time = models.FloatField(_("Slack"), blank=True, null=True)
	critical = models.CharField(max_length=255, blank=True, null=True)
	successors = models.CharField(max_length=255, blank=True, null=True)
	# excel_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

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


class Estimasi_Waktu(models.Model):
	kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, blank=False, null=True)
	# kode = models.CharField(max_length=255, blank=True, null=True)
	# tipe_estimasi = models.CharField(_("Tipe Estimasi"), max_length=255, choices=ESTIMATE_CHOICES, default="a", null=True, blank=True)
	# estimasi_waktu = models.IntegerField(_("Estimasi Waktu"))
	estimasi_waktu_a = models.FloatField(_("Optimistic Time"), blank=True, null=True)
	estimasi_waktu_m = models.FloatField(_("Most Likely Time"), blank=True, null=True)
	estimasi_waktu_b = models.FloatField(_("Pessismistic Time"), blank=True, null=True)


	class Meta:
		ordering = ('id',)
		verbose_name = 'Estimasi Waktu'
		verbose_name_plural = 'Estimasi Waktu'

	def __str__(self):
		return str(self.id)

	def get_durasi(self):
		return (self.estimasi_waktu_a + (self.estimasi_waktu_m*4) + self.estimasi_waktu_b)/6



class Estimasi_Biaya(models.Model):
	kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, blank=False, null=True)
	# kode = models.CharField(max_length=255, blank=True, null=True)
	# estimasi_biaya = models.IntegerField(_("Estimasi Biaya"))
	bcws = models.DecimalField(_("Budgeted Cost of Work Schedule"), max_digits=10, decimal_places=0)
	bcwp = models.DecimalField(_("Budgeted Cost of Work Planned "), max_digits=10, decimal_places=0)
	acwp = models.DecimalField(_("Actual Cost of Work Planned"), max_digits=10, decimal_places=0)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Estimasi Biaya'
		verbose_name_plural = 'Estimasi Biaya'

	# def __str__(self):
	#     return str(self.id)

	# @property
	# def price_display(self):
	#     return "Rp%s" % self.estimasi_biaya
