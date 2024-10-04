from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer
    queryset=Driver.objects.all()

    def get_object(self):
        return Driver.objects.get(user=self.request.user)
