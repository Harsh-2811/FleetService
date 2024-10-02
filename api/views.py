from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from fleet.models import *
from user.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.permissions import AllowAny,IsAuthenticated

# Create your views here.
class LoginUser(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class DriverDetails(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):

        id=request.user.id
        try:
            driver=Driver.objects.get(user__id=id)

            vehicle=Vehicle.objects.filter(driver=driver).first()
            
            driver_details={
                "name":driver.user.first_name,
                "id":driver.driver_id,
                "vehicle": {
                    "vehicle details":vehicle.plate_number,
                }
            }

            serializer=DriverSerializer(driver_details)
            return Response(serializer.data)
            
        except Exception as e:
            driver_details={
                "name":"",
                "id":"",
                "vehicle": {
                    "vehicle details":"",
                }
            }
            serializer=DriverSerializer(driver_details)
            return Response(serializer.data)

    