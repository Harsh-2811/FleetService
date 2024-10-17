from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.utils import timezone
from .serializer import *
from fleet.serializer import *
from jobs.models import *
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser

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
            return Response({"detail":"Please Start this job before start or end break."})
        today = datetime.datetime.now()

        break_type=self.request.data.get('break_type').lower()
        if break_type == 'start':
            instance.job_status=Job.JobStatus.BREAK
            instance.break_start=today
            instance.save()
        if break_type == 'end':
            if not instance.break_start:
                return Response({"detail":"Please Start break for this job before end."})
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
        resp = super().update(request, *args, **kwargs)
        return Response({
            "detail": "Job finished successfully."
        }, status=status.HTTP_200_OK)

class JobImageViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = JobImageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "detail": "Image uploaded successfully."
        }, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        return instance
    

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
        
class PrefillChecksView(CreateAPIView):
    serializer_class = PrefillChecksSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "detail": "Prefill checks saved successfully."
        }, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        if not Driver.objects.filter(user=self.request.user).exists():
            raise NotFound("Driver not found.")
        date = timezone.now().date()
        driver = Driver.objects.get(user=self.request.user)
        serializer.save(date=date, driver=driver)

class IsPrefillCheckedView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            parameters=[
                OpenApiParameter(name="check_type", type=str, location=OpenApiParameter.QUERY, required=True)
            ]
    )
    def get(self, request, *args, **kwargs):
        check_type = request.query_params.get("check_type", "start_day")
        return Response({
            "is_checked": PrefillChecks.objects.filter(driver__user=request.user, date=timezone.now().date(), check_type=check_type).exists()
        })
    
class StartJobView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StartJobV2Serializer
    queryset = Job.objects.all()

    def get_object(self, job_id):
        id = job_id
        try:
            job = Job.objects.get(id=id)
            return job
        except Job.DoesNotExist:
            raise NotFound("Job not found.")
        
    def get_queryset(self):
        return self.queryset.filter(driver__user=self.request.user)    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if not PrefillChecks.objects.filter(driver__user=request.user, date=timezone.now().date()).exists():
            return Response({
                "detail": "Please fill the checks before starting the job."
            }, status=status.HTTP_400_BAD_REQUEST)
        job = self.get_object(validated_data['job'])
        job.job_status = Job.JobStatus.RUNNING
        job.started_at = timezone.now()
        job.save()
        return Response({
            "detail": "Job started successfully."
        }, status=status.HTTP_200_OK)