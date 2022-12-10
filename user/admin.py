from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from allauth.account.models import *

from .models import *


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'full_name',
        'is_active',
    ]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(EmailAddress)
