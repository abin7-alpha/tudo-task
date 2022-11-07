from rest_framework import serializers
from commodity.api.serializers.commodity_serializer import CommoditySerializer
from retailer.models import Retailer
from commodity.models import Commodity

class RetailerSubSerializer(serializers.ModelSerializer):
    commodities = CommoditySerializer(many=True)
    class Meta:
        model = Retailer
        fields = '__all__'
