import json
import requests

from accounts.api.serializers.registration_serializer import RegistrationSerializer
from accounts.models import Account
from order.models import Customer

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST',])
@permission_classes([AllowAny,])
def registration_view(request):
    """Register new customer and returns access token and refresh token"""
    
    data = json.loads(request.body)
    serializer = RegistrationSerializer(
                    data=data,
                )

    response_data = {}

    msg = "New customer successfully registered"

    if serializer.is_valid():
        account = serializer.save_user()

        user = Account.objects.get(email=account.email)
        token = str(RefreshToken.for_user(user))
        name = account.first_name + account.last_name

        Customer.objects.create(user=user, name=name, email=account.email)

        url = "http://"+request.get_host()+"/api/token/refresh/"
        tranf_data = {"refresh": token}
        sent = requests.post(url, data=tranf_data)
        data = json.loads(sent.text)
        refresh = data.get("refresh")
        access = data.get("access")

        response_data['refresh'] = refresh
        response_data['access'] = access
        response_data['email'] = account.email
        response_data['response'] = msg

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        error_data = serializer.errors
        response_data = error_data
        return Response(response_data, status=status.HTTP_200_OK)
    