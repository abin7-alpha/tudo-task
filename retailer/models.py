from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Account

class Retailer(models.Model):
    firstName = models.CharField(max_length=50,null=False,blank=True)
    lastName = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True,)
    city =  models.CharField(null=True,blank=True,max_length=25)
    country = models.CharField(null=True,blank=True,max_length=25)
    pin = models.CharField(max_length=10,null=True,blank=True)
    icon = models.URLField(max_length=1028,null=True,blank=True)
    emailId = models.EmailField(null=False,unique=True,blank=True)
    primaryContactNumber = PhoneNumberField(null=True,blank=True)
    isMailVerified = models.BooleanField(default=False)
    isPhoneVerified = models.BooleanField(default=False)
    emailKey = models.CharField(null=True,blank=True,max_length=255)
    password = models.CharField(max_length=50,null=False,blank=False)
    otp = models.CharField(max_length=10,null=True,blank=True)
    otpGenTime = models.DateTimeField(auto_now=True)
    djangoUser = models.ForeignKey(Account, null=True,blank=False, related_name='django_user',on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.firstName != None and self.lastName != None:
            fullname = self.firstName+" "+self.lastName
        else:
            fullname = self.pk
        return str(fullname)

    @property
    def commodities(self):
        return self.commodity_set.all()
