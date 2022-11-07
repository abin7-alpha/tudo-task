from django.contrib import admin
from order.models import Customer, Order, OrderItem, ShippingAddress

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
