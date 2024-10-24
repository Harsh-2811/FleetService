from django.db import models
from user.models import User
# Create your models here.

class JobFormField(models.Model):
    class FieldsTypes(models.TextChoices):
        text="Text","Text"
        number="Number","Number"
        boolean="Boolean","Boolean"
        select="Select","Select"
    
    class UseCases(models.TextChoices):
        start_day = "start_day", "Start Day"
        finish_job = "finish_job", "Finish Job"
        finish_day = "finish_day", "Finish Day"

    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50,choices=FieldsTypes.choices)
    use_case = models.CharField(max_length=50,choices=UseCases.choices, default=UseCases.start_day)

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
    profile_picture = models.ImageField(upload_to='support_person/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_us')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Contact Us"

class ContactUsImage(models.Model):
    contact_us = models.ForeignKey(ContactUs, on_delete=models.CASCADE, related_name='contact_us_image')
    image = models.ImageField(upload_to='contact_us/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_us.user.username