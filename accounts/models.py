from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.managers import EmailManager, MyaccountManager, CustomerManager

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=150, verbose_name="first_name", blank=True)
    last_name = models.CharField(max_length=150, verbose_name="last_name", blank=True)
    email 			= models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined		= models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login		= models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin		= models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active		= models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyaccountManager()

    customer = CustomerManager()
    all_emails = EmailManager()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True