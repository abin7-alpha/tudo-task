from rest_framework import serializers

from order.models import OrderItem, Order
from commodity.models import Commodity

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']

    def create(self, validated_data):
        commodity = Commodity.objects.get(id=self.context.get("item_id"))
        order = Order.objects.get(id=self.context.get("order_id"))
        order_item = OrderItem.objects.create(commodity=commodity, order=order, **validated_data)
        order_item.save()

        return order_item
