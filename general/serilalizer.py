from rest_framework import serializers
from .models import *


class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['option_value']
        
class JobFormFieldSerializer(serializers.ModelSerializer):
    select_options = SelectOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobFormField
        fields = ['field_name', 'field_type', 'select_options']

class JobFormFieldRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFormField
        fields = ['id']