from rest_framework import serializers
from .models import *
from fleet.models import User

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['plate_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

class DriverSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer(many=True,read_only=True)
    user=UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ['driver_id', 'user','license_number','contact_number','vehicle']
