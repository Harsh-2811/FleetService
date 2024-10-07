from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from jobs.models import *

# Create your views here.
class StartJob(CreateAPIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer

    def perform_create(self, serializer):
        driver=Driver.objects.get(user=self.request.user)
        serializer.save(driver=driver)