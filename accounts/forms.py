from django import forms

from .models import *


class UserProfileEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a UserProfile object.

    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Do stuff with form instance here

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'full_name')


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'full_name', 'is_staff', 'is_active', 'date_joined')

    def is_valid(self):
        return super().is_valid()
