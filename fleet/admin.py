from django.contrib import admin
from .models import *

# Register your models here.
class DriverAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'driver_id',
        'license_number',
        'contact_number'
    ]
admin.site.register(Driver,DriverAdmin)
admin.site.register(Vehicle)