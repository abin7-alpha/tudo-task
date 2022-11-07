from rest_framework import serializers
from accounts.models import Account

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email']
        