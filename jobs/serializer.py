from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from general.serilalizer import *
from .models import *
import base64
from django.core.files.base import ContentFile
from fleet.serializer import *
from django.utils import timezone
from .utils import *

class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        # Check if the image is base64-encoded
        if isinstance(data, str) and data.startswith("data:application/pdf"):
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
    
class JobInfoFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInfo
        fields = ["form_field", "value"]

class JobInfoManySerializer(serializers.ModelSerializer):
    form_fields = JobInfoFieldsSerializer(many=True)
    filled_pdf = Base64FileField(write_only=True, required=False)
    class Meta:
        model = JobInfo
        fields = ["job", "form_fields", "filled_pdf"]

    def create(self, validated_data):
        user = self.context["request"].user
        filled_pdf = validated_data['filled_pdf']
        if Job.objects.filter(driver__user=user, job_status__in=[Job.JobStatus.RUNNING, Job.JobStatus.BREAK], job_date=timezone.now().date()).exists():
            raise serializers.ValidationError({
                "detail": "You already have a job running or on break for today."
            })
        form_fields = validated_data.pop("form_fields")
        job = validated_data.get("job")

        for form_field in form_fields:
            JobInfo.objects.create(job=job, form_field=form_field["form_field"], value=form_field["value"])
        
        job.job_status = Job.JobStatus.RUNNING
        job.filled_pdf = filled_pdf
        job.started_at = timezone.localtime(timezone.now())
        job.save()

        return job

class JobSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    job_info = JobInfoFieldsSerializer(many=True)
    
    load_time = serializers.SerializerMethodField()
    unload_time = serializers.SerializerMethodField()
    travel_time = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    class Meta:
        model = Job

        fields = ["id", "job_title", "vehicle", "job_data", "job_status", "job_date", "job_info", "load_time", "unload_time", "travel_time", "total_time", "arrived_site_time", "arrived_job_time"]

    def get_load_time(self, obj):
        return load_time(obj)

    def get_unload_time(self, obj):
        return unload_time(obj)

    def get_travel_time(self, obj):
        return travel_time(obj)

    def get_total_time(self, obj):
        return total_job_time(obj)
         
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
    
    
class FinishJobSerializer(serializers.ModelSerializer):
    # permission_class = [IsAuthenticated]
    # images = serializers.ListField(child=Base64ImageFieldSerializer(), write_only=True)
    form_fields = JobInfoFieldsSerializer(many=True, write_only=True)
    signature = Base64ImageFieldSerializer(write_only=True)

    class Meta:
        model = Job
        fields = ["finish_reason", "form_fields", "signature"]

    def update(self, instance, validated_data):
        # images = validated_data.pop("images")
        finish_reason = validated_data.get("finish_reason")
        form_fields = validated_data.pop("form_fields")

        # for image in images:
        #     JobImage.objects.create(job=instance, image=image, action_type=JobImage.ActionType.finish_job)

        for form_field in form_fields:
            JobInfo.objects.create(job=instance, **form_field)

        instance.job_status = Job.JobStatus.FINISHED
        instance.finished_at = timezone.localtime(timezone.now())
        instance.finish_reason = finish_reason
        instance.save()

        return instance


class JobImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=Base64ImageFieldSerializer(), write_only=True)
    
    class Meta:
        model = JobImage
        fields = ["job", "images", "action_type"]


    def create(self, validated_data):
        images = validated_data.pop("images")
        job = validated_data.get("job")
        action_type = validated_data.get("action_type")

        for image in images:
            JobImage.objects.create(job=job, image=image, action_type=action_type, submitted_at=timezone.localtime(timezone.now()))

        return job
    
class PrefillChecksFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefillChecks
        fields = ["field", "value"]

class ImageSerializer(serializers.Serializer):
    image = serializers.FileField()
    
class PrefillChecksSerializer(serializers.ModelSerializer):
    form_fields = PrefillChecksFieldsSerializer(many=True)
    precheck_images = serializers.ListField(child=Base64ImageFieldSerializer(), write_only=True, required=False)
    class Meta:
        model = PrefillChecks
        fields = ["form_fields", "check_type", "precheck_images"]

    def create(self, validated_data):
        form_fields = validated_data.pop("form_fields")
        driver = validated_data.get("driver")
        date = validated_data.get("date")
        precheck_images = validated_data.pop("precheck_images", [])
        for form_field in form_fields:
            PrefillChecks.objects.create(
                driver=driver,
                date=date,
                check_type = validated_data.get("check_type"),
                **form_field
            )
        for image in precheck_images:
            PrecheckImages.objects.create(driver=driver, date=date, image=image)
        return validated_data
        
class StartJobV2Serializer(serializers.Serializer):
    job = serializers.IntegerField()

class UploadPdfSerializer(serializers.ModelSerializer):
    filled_pdf = Base64FileField(write_only=True)
    class Meta:
        model = Job
        fields = ['filled_pdf']
        
class JobArrivalSerializer(serializers.Serializer):
    job = serializers.IntegerField()
    action_type = serializers.CharField()
    
