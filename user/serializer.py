from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import *
from fleet.models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        attrs['user'] = user
        
        return attrs

        