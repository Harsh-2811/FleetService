from rest_framework import serializers
from .models import *
import base64
from django.core.files.base import ContentFile

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

class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['option_value']
        
class JobFormFieldSerializer(serializers.ModelSerializer):
    select_options = SelectOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobFormField
        fields = ['id','field_name', 'use_case', 'field_type', 'select_options']


class SupportPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportPerson
        fields = ['id','name', 'contact_number', 'email', 'profile_picture']

class ContactUsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=Base64ImageFieldSerializer(), write_only=True)

    class Meta:
        model = ContactUs
        fields = ['id', 'message', 'contact_number', 'images']


    def create(self, validated_data):
        images = validated_data.pop("images")
        contact_us = super().create(validated_data)

        for image in images:
            ContactUsImage.objects.create(contact_us=contact_us, image=image)

        return contact_us