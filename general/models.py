from django.db import models

# Create your models here.

class JobFormField(models.Model):
    class FieldsTypes(models.TextChoices):
        text="text","Text"
        number="number","Number"
        boolean="boolean","Boolean"
        select="select","Select"
    
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50,choices=FieldsTypes.choices)

    def __str__(self):
        return self.field_name
    
class SelectOption(models.Model):
    job_form = models.ForeignKey(JobFormField, on_delete=models.CASCADE, related_name='select_options')
    option_value = models.CharField(max_length=100)

    def __str__(self):
        return self.option_value