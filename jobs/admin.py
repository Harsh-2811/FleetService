from django.contrib import admin
from .models import *

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=[
        'driver',
        'id',
        'job_title',
        'job_data',
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
        'job',
        'action_type',
    ]
admin.site.register(JobImage,JobImageAdmin)