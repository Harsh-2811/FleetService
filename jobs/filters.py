import django_filters
from .models import Job

class JobStatusFilter(django_filters.FilterSet):
    job_status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Job
        fields = ['job_status']