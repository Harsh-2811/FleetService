from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from django.utils import timezone
from .serializer import *
from fleet.serializer import *
from jobs.models import *
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound

class JobsView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobStatusFilter
    queryset=Job.objects.all()
    http_method_names=['get']

    def get_queryset(self):
        today = datetime.date.today()
        queryset = super().get_queryset()

        queryset = queryset.filter(
            driver__user=self.request.user,
            job_date=today,
        ) 
        return queryset

# StartJobView
class AddJobInfoViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=JobInfoManySerializer
    queryset=JobInfo.objects.all()
    http_method_names=['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(JobSerializer(instance).data, status=HTTP_200_OK)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance
        

class BreakJobView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=BreakJobSerializer
    queryset=Job.objects.all()
    http_method_names=['patch']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.started_at:
            return Response({"Error":"Please Start this job before start or end break."})
        today = datetime.datetime.now()

        break_type=self.request.data.get('break_type').lower()
        if break_type == 'start':
            instance.job_status=Job.JobStatus.BREAK
            instance.break_start=today
            instance.save()
        if break_type == 'end':
            if not instance.break_start:
                return Response({"Error":"Please Start break for this job before end."})
            instance.job_status=Job.JobStatus.RUNNING
            instance.break_end=today
            instance.save()
        return super().update(request, *args, **kwargs)

class FinishJobView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=FinishJobSerializer
    queryset=Job.objects.all()
    http_method_names=['patch']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.started_at:
            return Response({"Error":"Please Start this job before finished."})
            
        today = datetime.datetime.now()

        instance.job_status=Job.JobStatus.FINISHED
        instance.finished_at=today
        instance.save()
        return super().update(request, *args, **kwargs)

class JobImageViewSet(ModelViewSet):
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
    

class ActiveJobView(RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer

    def get_object(self):
        today = timezone.now().date()
        try:
            job = Job.objects.get(
                driver__user=self.request.user,
                job_date=today,
                job_status__in=[Job.JobStatus.BREAK, Job.JobStatus.RUNNING]
            )
            return job
        except Job.DoesNotExist:
            raise NotFound("No active job found for today.")