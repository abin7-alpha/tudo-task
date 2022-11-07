from django.db import models
from retailer.models import Retailer
from django.conf import settings

MEASURING_UNITS = (
    ("kg(s)", "Kilograms"),
    ("l(s)", "Literes"),
    ("c(s)", "Count"),
)

class Commodity(models.Model):
    retailer=models.ForeignKey(Retailer, on_delete=models.CASCADE) 
    name=models.CharField(null=False, max_length=200)
    description=models.CharField(null=True,max_length=1024)
    todays_price=models.FloatField(null=True)
    offer_price=models.FloatField(null=True)
    measuring_unit=models.CharField(null=False,max_length=100, default='Kg(s)', choices=MEASURING_UNITS)
    available_quantity=models.FloatField(null=True)
    min_available_qty=models.FloatField(null=False,default=1.0)
    max_available_qty=models.FloatField(null=True,default=available_quantity)
    max_qty_allowed_per_order=models.FloatField(null=True,default=settings.MAX_QUANTITY_ALLOWED_PER_ORDER)
    gst=models.FloatField(null=False,default=0)
    isActive=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)+" "+str(self.todays_price)

