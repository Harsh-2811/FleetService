from django.db import models
from user.models import User
import uuid,random

# Create your models here.

def generate_driver_id():
    return str(random.randint(1000000000, 9999999999))

class Driver(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='driver')
    driver_id = models.CharField(max_length=10, unique=True,default=generate_driver_id, editable=False)
    license_number=models.CharField(max_length=12)
    contact_number=models.CharField(max_length=12,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.driver_id:
            unique_id = str(uuid.uuid4())[-9:]
            self.driver_id = unique_id 
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name
    
class Vehicle(models.Model):
    class VehicleTypes(models.TextChoices):
        # left for value and right for lable in admin panel
        flated_truck="Flatbed Trucks","Flatbed Trucks"
        tail_lift_trucks="Tail-Lift Trucks","Tail-Lift Trucks"
        box_trucks="Box Trucks","Box Trucks"
        dump_trucks="Dump Trucks","Dump Trucks"
        semi_trailer_trucks="Semi-Trailer Trucks","Semi-Trailer Trucks"
        jumbo_trailer_trucks="Jumbo Trailer Trucks","Jumbo Trailer Trucks"
        tanker_trucks="Tanker Trucks","Tanker Trucks"
        refrigerated_trucks="Refrigerated Trucks","Refrigerated Trucks"

    vehicle_name=models.CharField(max_length=100,null=True,blank=True)
    vehicle_type=models.CharField(max_length=100,choices=VehicleTypes.choices,null=True,blank=True)
    plate_number=models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.plate_number}-{self.vehicle_name}"