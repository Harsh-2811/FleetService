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
        fields = ['id','field_name', 'use_case', 'field_type', 'select_options']


class SupportPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportPerson
        fields = ['id','name', 'contact_number', 'email']

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'message']