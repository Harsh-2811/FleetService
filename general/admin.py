from django.contrib import admin
from .models import *

# Register your models here.

class SelectOptionInline(admin.TabularInline):
    model = SelectOption
    extra = 1

class JobFormAdmin(admin.ModelAdmin):
    list_display = ('id','field_name', 'field_type')
    inlines = [SelectOptionInline]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'field_type':
            kwargs['choices'] = JobFormField.FieldsTypes.choices
        return super().formfield_for_dbfield(db_field, request, **kwargs)

admin.site.register(JobFormField,JobFormAdmin)