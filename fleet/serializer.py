from rest_framework import serializers
from .models import *
from fleet.models import User
# from jobs.serializer import *

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','vehicle_name','vehicle_type','plate_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

