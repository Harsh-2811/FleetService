from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from .serializer import *
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from jobs.serializer import *

# Create your views here.
class DriverDetails(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DriverSerializer
    
    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound(detail="Driver not found")

class JobHistory(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = JobHistorySerializer

    
    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound(detail="Driver not found")
