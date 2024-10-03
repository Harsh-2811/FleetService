from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):

        try:
            driver=Driver.objects.get(user=request.user)
            if driver is not None:
                serializer=DriverSerializer(driver)
                return Response(serializer.data)
            
        except Exception as e :
            return Response({
                "error":e
            })