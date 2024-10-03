from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):

        id=request.user.id  
        driver=Driver.objects.get(user__id=id)

        serializer=DriverSerializer(driver)
        return Response(serializer.data)