from rest_framework import serializers

from order.models import ShippingAddress, Customer, Order
from accounts.models import Account

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

    def create(self, validated_data):
        user = Account.objects.get(email=self.context.get("email"))
        customer = Customer.objects.get(user=user)
        order = Order.objects.get(id=self.context.get("order_id"))
        ship = ShippingAddress.objects.create(customer=customer, order=order, **validated_data)
        ship.save()

        return ship
        