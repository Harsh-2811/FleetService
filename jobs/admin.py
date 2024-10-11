from django.contrib import admin
from .models import *
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'driver',
        'job_title',
        'job_status',
        'vehicle_plate_number',
    ]
    

    def vehicle_plate_number(self, obj):
        return obj.vehicle.plate_number  # Access the vehicle's plate number field
    vehicle_plate_number.short_description = 'Vehicle Plate Number' 
    
    list_filter=[
        'driver',
        # ('job_time',admin.DateFieldListFilter),
        'vehicle__vehicle_name',
        ('started_at',DateRangeFilterBuilder()),
        ('break_start',DateRangeFilterBuilder()),
        'job_status',
    ]

    date_hierarchy ='started_at'
    
    autocomplete_fields =[
        'driver',
        'vehicle',
    ]

    search_fields =[
        'driver__user__first_name',
        'driver__user__last_name',
    ]
    
admin.site.register(Job,JobAdmin)

class JobInfoAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'job',
        'form_field',
        'value',
    ]
    
admin.site.register(JobInfo,JobInfoAdmin)

class JobImageAdmin(admin.ModelAdmin):
    list_display=[
        'job_id',
        'action_type',
    ]

admin.site.register(JobImage,JobImageAdmin)