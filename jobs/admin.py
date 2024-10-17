from django.contrib import admin
from .models import *
from rangefilter.filters import (
    DateRangeFilterBuilder,
)
from django.utils.html import format_html

class JobImageInline(admin.TabularInline):
    model = JobImage
    extra = 0
    fields = ['image', 'output_image'] 
    readonly_fields = ['output_image']    

    def output_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100">'.format(obj.image.url))
        return "No Image" 

class JobInfoInline(admin.TabularInline):
    model = JobInfo
    extra = 0
    fields = ['form_field', 'value', 'use_case']
    readonly_fields = ['use_case']  

    def use_case(self, obj):
        return obj.form_field.get_use_case_display()  

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=[
        'driver',
        'job_title',
        'job_status',
        'vehicle_plate_number',
    ]
    
    inlines = [JobImageInline, JobInfoInline]
    def vehicle_plate_number(self, obj):
        return obj.vehicle.plate_number  # Access the vehicle's plate number field
    vehicle_plate_number.short_description = 'Vehicle Plate Number' 

    def signature_thumbnail(self, obj):
        if obj.signature:
            return format_html('<img src="{}" width="150" style="border-radius: 5px;" />'.format(obj.signature.url))
        return "No Signature"
    signature_thumbnail.short_description = 'Signature'

    readonly_fields = ['signature_thumbnail']
    
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

class PrefillChecksAdmin(admin.ModelAdmin):
    list_display=[
        'driver',
        'field',
        'value',
        'created_at',
    ]

admin.site.register(PrefillChecks, PrefillChecksAdmin)