from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import login
from fleet.models import *
from user.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.permissions import AllowAny

# Create your views here.
class LoginUser(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        login(self.request,user)
        try:
            driver = Driver.objects.get(user=user)
        except Driver.DoesNotExist:
            driver = None
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'driver': {
                "driver_id": driver.driver_id,
                "license_number": driver.license_number,
                "contact_number": driver.contact_number,
            }
        })