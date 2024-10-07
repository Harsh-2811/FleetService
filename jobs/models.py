from django.db import models
from django.utils import timezone
from fleet.models import Driver
from general.models import *
from .models import *

class Job(models.Model):
    class JobStatus(models.TextChoices):
        ASSIGNED = 'Assigned', 'Assigned'
        RUNNING = 'Running', 'Running'
        FINISHED = 'Finished', 'Finished'
        BREAK = 'Break', 'Break'

    job_title = models.CharField(max_length=150,null=True,blank=True)
    job_data = models.TextField(max_length=200,null=True,blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='jobs')

    job_status = models.CharField(max_length=10,choices=JobStatus.choices,default=JobStatus.ASSIGNED)

    job_time = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    break_start = models.DateTimeField(null=True, blank=True)
    break_end = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.driver.user.first_name} - {self.job_data} - {self.job_status}"

class JobInfo(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_info')
    form_field = models.ForeignKey(JobFormField, on_delete=models.CASCADE, related_name='job_info')
    value = models.CharField(max_length=255)

    def parse_value(self):
        if self.form_field.field_type == JobFormField.FieldsTypes.text:
            return self.values
        elif self.form_field.field_type == JobFormField.FieldsTypes.number:
            try:
                return int(self.value)
            except ValueError:
                raise ValueError(f"Invalid number value: {self.value}")
        elif self.form_field.field_type == JobFormField.FieldsTypes.boolean:
            if self.value.lower() == "true":
                return True
            elif self.value.lower() == "false":
                return False
            else:
                raise ValueError(f"Invalid boolean value: {self.value}")
        else:
            return self.value

    def __str__(self):
        return f"Job_Field: {self.form_field.field_name}, Value: {self.value}"
