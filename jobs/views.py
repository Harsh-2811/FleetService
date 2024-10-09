from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
import datetime
from .serializer import *
from jobs.models import *
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiExample

class Jobs(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    
    def get_queryset(self):
        try:
            today = datetime.datetime.today()
            return Job.objects.filter(driver__user=self.request.user,created_at__date=today).order_by('created_at').reverse()
        except Driver.DoesNotExist:
            raise NotFound(detail="Jobs are not found created today.")

# StartJobView
class AddJobInfoView(APIView):
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
        request=JobInfoSerializer,  # Define the request body schema here
        responses={201: JobInfoSerializer},  # Define the response schema
        examples=[
            OpenApiExample(
                'Start Job and Add Job Info',
                value={
                    "job_info": [
                        {
                            "form_field":1,
                            "value":"value"
                        }
                    ],
                },
                request_only=True
            )
        ]
    )
    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
            job.job_status=Job.JobStatus.RUNNING
            job.started_at=datetime.datetime.now()
            job.save()
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
        
        return Response({'message': 'Job is Started and Job info added successfully...'})

class BreakJobView(APIView):
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
        request=JobInfoSerializer,  # Define the request body schema here
        responses={201: JobInfoSerializer},  # Define the response schema
        examples=[
            OpenApiExample(
                'Start or End Job.',
                value={
                        "break_type":"start"
                    },
                request_only=True
            )
        ]
    )
    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'})

        try:
            break_type = request.data.get('break_type').lower()
            if break_type == 'start':
                job.job_status=Job.JobStatus.BREAK
                job.break_start=datetime.datetime.now()
                job.save()
                return Response({'message': 'Job Break is Started...'})
            elif break_type == 'end':
                job.job_status=Job.JobStatus.RUNNING
                job.break_end=datetime.datetime.now()
                job.save()
                return Response({'message': 'Job Break is Ended...'})
            else:
                return Response({'message': 'Enter Proper Break Type...'})

        except Exception as e:
            return Response({"Error":"Payload should be a break_type key and type pair value."})

class FinishJobView(APIView):
    permission_classes=[IsAuthenticated]
    serialzer_class=JobSerializer

    def patch(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
            job.job_status=Job.JobStatus.FINISHED
            job.finished_at=datetime.datetime.now()
            job.save()
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'})

        return Response({'message': 'Job Finished...'})

# ModelViewSet
class JobImageViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = JobImageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        action_type = request.data.get('action_type')
        images = request.FILES.getlist('images')

        try:
            job=request.data.get('job')
        except Exception as e:
            return Response({"error": "job_id is not provided."})

        if not images:
            return Response({"error": "No images provided."})

        responses = []
        for image in images:

            data = {'job':job,'image': image, 'action_type': action_type}
            serializer = self.get_serializer(data=data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                responses.append(serializer.data)
            else:
                return Response(serializer.errors)

        return Response(responses)

