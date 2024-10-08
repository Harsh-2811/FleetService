from rest_framework.generics import ListAPIView,UpdateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
import datetime
from .serializer import *
from jobs.models import *

class Jobs(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    
    def get_queryset(self):
        try:
            today = datetime.datetime.today()
            return Job.objects.filter(driver__user=self.request.user,created_at__date=today).order_by('created_at').reverse()
        except Driver.DoesNotExist:
            raise NotFound(detail="Jobs are not found created today.")


from rest_framework.views import APIView

class AddJobInfoView(APIView):
    
    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'})

        data = request.data.get('job_info', [])

        if not isinstance(data, list):
            return Response({'error': 'job_info should be a list of form_field_id and value pairs'})
        
        errors = []
        
        for entry in data:
            serializer = JobInfoSerializer(data=entry, context={'job': job})
            
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
        
        if errors:
            return Response({'errors': errors})
        
        return Response({'message': 'Job info successfully added'})