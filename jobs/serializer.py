from rest_framework import serializers
from general.serilalizer import *
from .models import *
import base64
from rest_framework.response import Response
from django.core.files.base import ContentFile
        
class JobInfoSerializer(serializers.Serializer):
    form_field_id = serializers.IntegerField()
    value = serializers.CharField()

    def validate_form_field_id(self, value):
        # Check if the form field exists
        try:
            JobFormField.objects.get(id=value)
        except JobFormField.DoesNotExist:
            raise serializers.ValidationError(f"Form field with ID {value} does not exist.")
        return value

    def create(self, validated_data):
        # Assuming validated_data has 'job' passed in context
        job = self.context.get('job')
        form_field = JobFormField.objects.get(id=validated_data['form_field_id'])
        return JobInfo.objects.create(
            job=job,
            form_field=form_field,
            value=validated_data['value']
        )


class JobSerializer(serializers.ModelSerializer):
    job_info=JobInfoSerializer(many=True,read_only=True)

    class Meta:
        model = Job
        fields=['id','job_title','job_data','job_status','job_info','job_time']


class Base64ImageFieldSerializer(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if the image is base64-encoded
        if isinstance(data, str) and data.startswith('data:image'):
            # Decoding base64-encoded image
            format, imgstr = data.split(';base64,')  # Split the format from the base64 content
            ext = format.split('/')[-1]  # Extract the file extension (e.g., 'jpeg', 'png')
            # Create a ContentFile from the base64 string
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

        return super().to_internal_value(data)

class JobImageSerializer(serializers.ModelSerializer):
    image=Base64ImageFieldSerializer()
    class Meta:
        model = JobImage
        fields = ['job','image', 'action_type']
        
    def validate(self, attrs):
        request = self.context.get('request')
        action_type = attrs.get('action_type')
        images = request.FILES.getlist('images')

        if action_type == JobImage.ActionType.arrive_job and len(images) > 4:
            raise serializers.ValidationError("You can upload a maximum of 4 images for Arrive Job.")
        
        if action_type == JobImage.ActionType.arrive_site and len(images) > 5:
            raise serializers.ValidationError("You can upload a maximum of 5 images for Arrive Site.")

        return attrs
