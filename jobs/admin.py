import io
import os
import zipfile
from django.urls import path
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from rangefilter.filters import (
    DateRangeFilterBuilder,
)
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone


class JobImageInline(admin.TabularInline):
    model = JobImage
    extra = 0
    fields = ['image', 'output_image', 'download_image'] 
    readonly_fields = ['output_image', 'download_image']    

    def output_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100">'.format(obj.image.url))
        return "No Image" 
    
    def download_image(self, obj):
        if obj.image:
            return format_html(
                f'<a class="button" href="{obj.image.url}" download style="color:#fff">Download</a>',
            )
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

    def arrived_job_time(self, obj: Job):
        arrived_job = JobImage.objects.filter(job=obj, action_type=JobImage.ActionType.arrive_job).first()
        if not arrived_job:
            return "No Arrived Job Time"
        return timezone.localtime(arrived_job.submitted_at).strftime("%B %d, %Y, %I:%M %p") if arrived_job else None

    def load_time(self, obj: Job):
        arrived_job = JobImage.objects.filter(job=obj, action_type=JobImage.ActionType.arrive_job).first()
        if not arrived_job:
            return "No Load Time"
        arrived_job_time = arrived_job.submitted_at if arrived_job else None
        arrived_job_time = timezone.localtime(arrived_job_time) if arrived_job_time else None
        departed_at = obj.departed_at if obj.departed_at else None

        # Calculate load time, out should be HH:MM
        if arrived_job_time and departed_at:
            load_time = departed_at - arrived_job_time
            hours, remainder = divmod(load_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return "No Load Time"
    load_time.short_description = 'Load Time'

    readonly_fields = ['signature_thumbnail', 'started_at',
        'arrived_job_time',
        'departed_at',
        'load_time',
        'finished_at',
        'break_start',
        'break_end',
        'finish_reason',
        'signature']
    
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'download-images/<int:job_id>/',
                self.admin_site.admin_view(self.download_images_view),
                name='download-job-images',
            ),
        ]
        return custom_urls + urls
    
    def download_images_view(self, request, job_id):
        job = Job.objects.get(id=job_id)
        images = JobImage.objects.filter(job=job)
        
        # Create in-memory zip file
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for image in images:
                image_name = os.path.basename(image.image.name)
                zip_file.writestr(image_name, image.image.read())
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{job.id}_images.zip"'
        return response
    
    # Button in change list view
    def download_images_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Download Images</a>',
            reverse('admin:download-job-images', args=[obj.pk])
        )
    download_images_button.short_description = 'Download Images'
    download_images_button.allow_tags = True
    
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