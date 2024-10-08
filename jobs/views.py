from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
import datetime
from .serializer import *
from jobs.models import *
from rest_framework.views import APIView
from rest_framework import viewsets
import json

from drf_spectacular.utils import extend_schema


class Jobs(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    
    def get_queryset(self):
        try:
            today = datetime.datetime.today()
            return Job.objects.filter(driver__user=self.request.user,created_at__date=today).order_by('created_at').reverse()
        except Driver.DoesNotExist:
            raise NotFound(detail="Jobs are not found created today.")

class AddJobInfoView(APIView):
    
    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
            job.job_status=Job.JobStatus.RUNNING
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

# ModelViewSet
class JobImageViewSet(viewsets.ModelViewSet):
    queryset = JobImage.objects.all()
    serializer_class = JobImageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        action_type = request.data.get('action_type')
        images = request.FILES.getlist('images')


        try:
            job_id=request.data.get('job_id')
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job with the specified ID does not exist."})

        if not images:
            return Response({"error": "No images provided."})

        responses = []
        for image in images:

            data = {'job':job_id,'image': image, 'action_type': action_type}
            serializer = self.get_serializer(data=data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                responses.append(serializer.data)
            else:
                return Response(serializer.errors)

        return Response(responses)

