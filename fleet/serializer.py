from rest_framework import serializers
from .models import *
from fleet.models import User
from jobs.serializer import *

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','vehicle_name','vehicle_type','plate_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

class DriverSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            'user',
            'driver_id', 
            'license_number',
            'contact_number',
            'vehicles',
        ]

    def get_vehicles(self, obj):
        jobs = Job.objects.filter(driver=obj)
        vehicles = set([job.vehicle for job in jobs])
        return VehicleSerializer(vehicles, many=True).data

class JobHistorySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    vehicles = serializers.SerializerMethodField()
    jobs = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            'user',
            'driver_id', 
            'license_number',
            'contact_number',
            'jobs',
            'vehicles',
        ]

    def get_vehicles(self, obj):
        jobs = Job.objects.filter(driver=obj)
        vehicles = set([job.vehicle for job in jobs])
        return VehicleSerializer(vehicles, many=True).data

    def get_jobs(self, obj):
        jobs = Job.objects.filter(driver=obj,job_status=Job.JobStatus.FINISHED)
        return JobSerializer(jobs, many=True).data
        
