import django_filters   
from .models import JobFormField

class JobFormFieldFilter(django_filters.FilterSet):
    class Meta:
        model = JobFormField
        fields = ['use_case']