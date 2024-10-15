from django.db import models
from user.models import User
# Create your models here.

class JobFormField(models.Model):
    class FieldsTypes(models.TextChoices):
        text="Text","Text"
        number="Number","Number"
        boolean="Boolean","Boolean"
        select="Select","Select"
    
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50,choices=FieldsTypes.choices)

    def __str__(self):
        return self.field_name
    
class SelectOption(models.Model):
    job_form = models.ForeignKey(JobFormField, on_delete=models.CASCADE, related_name='select_options')
    option_value = models.CharField(max_length=100)

    def __str__(self):
        return self.option_value
    
class SupportPerson(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_us')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name