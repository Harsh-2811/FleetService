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

    search_fields=[
        'user__first_name',
        'user__last_name',
    ]

admin.site.register(Driver,DriverAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_display=[
        'vehicle_name',
        'plate_number',
        'vehicle_type',
    ]

    search_fields=[
        'plate_number',
    ]

admin.site.register(Vehicle,VehicleAdmin)