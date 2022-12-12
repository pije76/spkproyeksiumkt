from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager
# from proyek.models import *

# Create your models here.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=30, help_text=_('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'), blank=False, unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    # nama_proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, blank=True, null=True)


    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _("Account")

    # def __str__(self):
        # return str(self.full_name)
        # return self.id

    def get_full_name(self):
      full_name = '%s %s' % (self.first_name, self.last_name)
      return full_name.strip()
      # return self.email
