from django.db import models
from user.models import User
import uuid,random,string

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
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,related_name='vehicle')
    plate_number=models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.driver.user.first_name}  {self.plate_number}"