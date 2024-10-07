from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
import datetime
from .serializer import *
from jobs.models import *

# Create your views here.
class StartJob(CreateAPIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer

    def perform_create(self, serializer):
        driver=Driver.objects.get(user=self.request.user)
        serializer.save(driver=driver)

class Jobs(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    
    def get_queryset(self):
        try:
            today = datetime.datetime.today()
            return Job.objects.filter(driver__user=self.request.user,created_at__date=today).order_by('created_at').reverse()
        except Driver.DoesNotExist:
            raise NotFound(detail="Jobs are not found created today.")