from django.db import models

from accounts.models import *

# Create your models here.
class Proyek(models.Model):
    nama_proyek = models.CharField(max_length=255, blank=True, null=True)
    SPK = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return str(self.nama_proyek)
