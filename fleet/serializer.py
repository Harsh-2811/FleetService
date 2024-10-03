from rest_framework import serializers
from .models import *

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['plate_number']

class DriverSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer(many=True,read_only=True)

    class Meta:
        model = Driver
        fields = ['driver_id', 'license_number','contact_number','vehicle']
