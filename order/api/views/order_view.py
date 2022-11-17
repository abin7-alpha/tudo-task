import json

from order.api.serializers.order_serializer import OrderSerializer
from order.api.serializers.orderitem_serializer import OrderItemSerializer
from order.api.serializers.shipping_serializer import ShippingAddressSerializer

from accounts.models import Account
from order.models import Customer
from commodity.models import Commodity

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def order_view(request):
    """Create the order by giving these data 
    {
        "email": "demo@gmail.com",
        "items": [
            {
                "item_id": 1,
                "quantity": 10
            },
            {
                "item_id": 3,
                "quantity": 10
            }
        ],
        "transaction_id": 2345,
        "address": "hilal nagr house",
        "city": "thhrikur",
        "state": "kerala",
        "zipcode": "680302"
    }
    these are the required datas"""

    data = json.loads(request.body)

    order_serializer = OrderSerializer(data=data, context=data)

    user = Account.objects.get(email=data["email"])

    for item in data["items"]:
        commodity = Commodity.objects.get(id=item["item_id"])
        response_data = {}

        # if item["quantity"] > commodity.max_qty_allowed_per_order:
        #     response_data["error"] = f"{commodity.name} quantity should be under the limit ${commodity.max_qty_allowed_per_order}"
        #     return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if item["quantity"] > commodity.max_available_qty:
            response_data["error"] = f"{commodity.name}'s maximum available quantity is {commodity.max_available_qty}"
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if commodity.available_quantity < item["quantity"]:
            response_data["error"] = f"{commodity.name} is out of stock, We will notify you when it arrives"
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        available_quantity = commodity.available_quantity - float(item["quantity"])
        Commodity.objects.filter(id=item["item_id"]).update(available_quantity=available_quantity, max_available_qty=available_quantity)

    if order_serializer.is_valid():
        
        order = order_serializer.save()

        data.update({"order_id": order.id})

        for item_data in data["items"]:
            item_data.update({"order_id": order.id})
            order_item_serializer = OrderItemSerializer(data=item_data, context=item_data)

            if order_item_serializer.is_valid():
                order_item_serializer.save()
            else:
                response_data = order_item_serializer.errors
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        shipping_serializer = ShippingAddressSerializer(data=data, context=data)
        
        if shipping_serializer.is_valid():
            shipping_serializer.save()
        else:
            response_data = shipping_serializer.errors
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {}

        response_data["msg"] = "Successfully ordered item"
        response_data["transaction_id"] = order.transaction_id

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {}

        if order_serializer.errors():
            response_data = order_serializer.errors()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
