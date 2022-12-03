from django.db import models

# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email Address', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
    username = models.CharField(max_length=30, help_text=_('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'), validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')], unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    objects = UserManager()
    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _("User Profile")

    # def __str__(self):
    #   return self.username
        # return str(self.username)
        # return "User profile: %s" % self.username
        # return self.email

    # def clean(self):
    #   super().clean()
    #   self.sun_sign = self.full_name
    #   self.email = self.__class__.objects.normalize_email(self.email)

    def clean_title(self):
        return self.cleaned_data['full_name'].capitalize()
