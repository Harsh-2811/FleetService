from rest_framework import serializers
from general.serilalizer import *
from .models import *


class JobInfoSerializer(serializers.ModelSerializer):
    form_field=JobFormFieldSerializer()
    class Meta:
        model = JobInfo
        fields=['form_field','value']

class JobSerializer(serializers.ModelSerializer):
    job_info=JobInfoSerializer(many=True,read_only=True)

    class Meta:
        model = Job
        fields=['job_title','job_data','job_status','job_info','job_time']