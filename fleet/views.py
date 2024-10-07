from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializer import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer
    queryset=Driver.objects.all()

    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound(detail="Driver not found")
