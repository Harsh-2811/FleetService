from rest_framework import serializers
from .models import *


class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['id', 'option_value']
        

class JobFormFieldSerializer(serializers.ModelSerializer):
    select_options = SelectOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobFormField
        fields = ['id', 'field_name', 'field_type', 'select_options']