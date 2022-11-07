import json
import requests

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from retailer.models import Retailer
from accounts.models import Account
from accounts.api.serializers.sub_serializer import RetailerSubSerializer

from order.models import Customer

def retailer_by_commodities():
    retailers = Retailer.objects.all()
    serializer = RetailerSubSerializer(retailers, many=True)
    return serializer.data

@api_view(['POST',])
@permission_classes([AllowAny,])
def login_view(request):
    """Login the user and returns list of commodities by the user"""
    data = json.loads(request.body)

    response_data = {}

    try:
        user = Account.objects.get(email=data["email"])
    except:
        return Response({"error": "Account with this email does'nt exist."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        authorize = authenticate(email=data["email"], password=data["password"])
        if authorize == None:
            raise Exception("Incorrect password")
    except Exception as error:
        return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)


    if authorize:
        url = "http://"+request.get_host()+"/api/token/"
        tranf_data = data
        sent = requests.post(url, data=tranf_data)
        data = json.loads(sent.text)
        refresh = data.get("refresh")
        access = data.get("access")

        #Returns the list of commodities by the retailer
        main_data = retailer_by_commodities()

        response_data["access"] = access
        response_data["refresh"] = refresh
        response_data["email"] = user.email
        response_data["data"] = main_data
        response_data["msg"] = "Succesfully Auntheticated"

        return Response(response_data, status=status.HTTP_200_OK)
    
    else:
        return ValidationError({"error": "Account does'nt exist."})
