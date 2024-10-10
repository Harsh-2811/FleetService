from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from .serializer import *
from jobs.models import *
from rest_framework.viewsets import ModelViewSet

class JobsView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=JobSerializer
    queryset=Job.objects.all()
    http_method_names=['get']

    def get_queryset(self):
        today = datetime.datetime.today()
        queryset = super().get_queryset()

        job_status=self.request.data.get('job_status').capitalize()
        print("Job Status is ",job_status)
        queryset = queryset.filter(
            driver__user=self.request.user,
            created_at__date=today,
            job_status=job_status
        ) 
        return queryset

# StartJobView
class AddJobInfoViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=JobInfoSerializer
    http_method_names=['post']

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