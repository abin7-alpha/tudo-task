from rest_framework import serializers

from order.models import Order, Customer
from accounts.models import Account

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['transaction_id']

    def create(self, validated_data):
        user = Account.objects.get(email=self.context.get("email"))
        customer = Customer.objects.get(user=user)
        order = Order.objects.create(customer=customer, complete=False,**validated_data)
        order.save()

        return order
