from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from general.serilalizer import *
from .models import *
import base64
from django.core.files.base import ContentFile
from fleet.serializer import *
from django.utils import timezone


class JobInfoFieldsSerializer(serializers.ModelSerializer):
    permission_class = [IsAuthenticated]

    class Meta:
        model = JobInfo
        fields = ["form_field", "value"]

class JobInfoManySerializer(serializers.ModelSerializer):
    form_fields = JobInfoFieldsSerializer(many=True)

    class Meta:
        model = JobInfo
        fields = ["job", "form_fields"]

    def create(self, validated_data):
        user = self.context["request"].user
        if Job.objects.filter(driver__user=user, job_status__in=[Job.JobStatus.RUNNING, Job.JobStatus.BREAK], job_date=timezone.now().date()).exists():
            raise serializers.ValidationError({
                "detail": "You already have a job running or on break for today."
            })
        form_fields = validated_data.pop("form_fields")
        job = validated_data.get("job")

        for form_field in form_fields:
            JobInfo.objects.create(job=job, **form_field)
        
        job.job_status = Job.JobStatus.RUNNING
        job.started_at = timezone.now()
        job.save()

        return job

class JobSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    job_info = JobInfoFieldsSerializer(many=True)
    class Meta:
        model = Job

        fields = ["id", "job_title", "vehicle", "job_data", "job_status", "job_date", "job_info"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        job_images = JobImage.objects.filter(job=instance, action_type=JobImage.ActionType.arrive_job).values_list("image", flat=True)
        response["job_images"] = list(job_images)
        site_images = JobImage.objects.filter(job=instance, action_type=JobImage.ActionType.arrive_site).values_list("image", flat=True)
        response["site_images"] = list(site_images)
        return response

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            "user",
            "driver_id",
            "license_number",
            "contact_number",
            "vehicles",
        ]

    def get_vehicles(self, obj):
        jobs = Job.objects.filter(driver=obj)
        vehicles = set([job.vehicle for job in jobs])
        return VehicleSerializer(vehicles, many=True).data


class JobHistorySerializer(serializers.ModelSerializer):
    jobs = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            "jobs",
        ]

    def get_vehicles(self, obj):
        jobs = Job.objects.filter(driver=obj)
        vehicles = set([job.vehicle for job in jobs])
        return VehicleSerializer(vehicles, many=True).data

    def get_jobs(self, obj):
        jobs = Job.objects.filter(driver=obj, job_status=Job.JobStatus.FINISHED)
        return JobSerializer(jobs, many=True).data


class BreakJobSerializer(serializers.ModelSerializer):
    permission_class = [IsAuthenticated]

    class Meta:
        model = Job
        fields = ["break_start", "break_end", "job_status"]


class FinishJobSerializer(serializers.ModelSerializer):
    permission_class = [IsAuthenticated]

    class Meta:
        model = Job
        fields = ["started_at", "finished_at", "job_status"]


class Base64ImageFieldSerializer(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if the image is base64-encoded
        if isinstance(data, str) and data.startswith("data:image"):
            # Decoding base64-encoded image
            format, imgstr = data.split(
                ";base64,"
            )  # Split the format from the base64 content
            ext = format.split("/")[
                -1
            ]  # Extract the file extension (e.g., 'jpeg', 'png')
            # Create a ContentFile from the base64 string
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        return super().to_internal_value(data)


class JobImageSerializer(serializers.ModelSerializer):
    image = Base64ImageFieldSerializer()

    class Meta:
        model = JobImage
        fields = ["job", "image", "action_type"]

    def validate(self, attrs):
        request = self.context.get("request")
        action_type = attrs.get("action_type")
        job = request.data.get("job")
        try:
            images = JobImage.objects.filter(job=job, action_type=action_type)
            if action_type == JobImage.ActionType.arrive_job and len(images) == 4:
                raise serializers.ValidationError(
                    "Images for Arrive Job  is already exists."
                )

            if action_type == JobImage.ActionType.arrive_site and len(images) == 5:
                raise serializers.ValidationError(
                    "Images for Arrive Site  is already exists."
                )

        except Exception as e:
            raise serializers.ValidationError(
                f"Images are already exists for {action_type}"
            )

        images = request.FILES.getlist("images")
        if action_type == JobImage.ActionType.arrive_job and len(images) > 4:
            raise serializers.ValidationError(
                "You can upload a maximum of 4 images for Arrive Job."
            )

        if action_type == JobImage.ActionType.arrive_site and len(images) > 5:
            raise serializers.ValidationError(
                "You can upload a maximum of 5 images for Arrive Site."
            )

        if action_type == JobImage.ActionType.arrive_job and len(images) < 4:
            raise serializers.ValidationError(
                "You have to upload 4 images for Arrive Job."
            )

        if action_type == JobImage.ActionType.arrive_site and len(images) < 5:
            raise serializers.ValidationError(
                "You have to upload 5 images for Arrive Site."
            )

        return attrs
