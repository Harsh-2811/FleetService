from django.db import models
from user.models import User
import uuid,random

# Create your models here.

def generate_driver_id():
    return str(random.randint(1000000000, 9999999999))

class Driver(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='user')
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
        flated_truck="flatbed_truck","Flatbed Trucks"
        number="number","Tail-Lift Trucks"
        boolean="box_trucks","Box Trucks"
        dump_trucks="dump_trucks","Dump Trucks"
        semi_trailer_trucks="semi_trailer_trucks","Semi-Trailer Trucks"
        jumbo_trailer_trucks="jumbo_trailer_trucks","Jumbo Trailer Trucks"
        tanker_trucks="tanker_trucks","Tanker Trucks"
        refrigerated_trucks="refrigerated_trucks","Refrigerated Trucks"

    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,related_name='vehicle')
    vehicle_name=models.CharField(max_length=100,null=True,blank=True)
    vehicle_type=models.CharField(max_length=100,choices=VehicleTypes.choices,null=True,blank=True)
    plate_number=models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.driver.user.first_name}-{self.vehicle_name}"