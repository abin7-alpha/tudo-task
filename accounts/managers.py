from django.db import models
from django.contrib.auth.models import BaseUserManager

class MyaccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email, password):
        email = self.normalize_email(email)
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False).filter(is_admin=False)

class EmailManager(models.Manager):
    def only(self):
        return super().only("email")
        