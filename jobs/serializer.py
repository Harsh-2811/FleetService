from rest_framework import serializers
from general.serilalizer import *
from .models import *
        
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

