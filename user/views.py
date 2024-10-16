from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from fleet.models import Driver
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status


# Create your views here.
class LoginUser(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        try:
            driver = Driver.objects.get(user=user)
        except Driver.DoesNotExist:
            return Response(
                {"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "driver": {
                    "driver_id": driver.driver_id,
                    "license_number": driver.license_number,
                    "contact_number": driver.contact_number,
                },
            },
            status=status.HTTP_200_OK,
        )
