from django.contrib import admin
from .models import *
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ContactUsImageInline(admin.TabularInline):
    model = ContactUsImage
    extra = 0
    fields = ['image', 'output_image'] 
    readonly_fields = ['output_image']    

    def output_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100">'.format(obj.image.url))
        return "No Image"

class SelectOptionInline(admin.TabularInline):
    model = SelectOption
    extra = 1

class JobFormAdmin(ImportExportModelAdmin):
    list_display = ('id','field_name', 'field_type', 'use_case')
    list_editable = ('field_name', 'field_type', 'use_case')

    inlines = [SelectOptionInline]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'field_type':
            kwargs['choices'] = JobFormField.FieldsTypes.choices
        return super().formfield_for_dbfield(db_field, request, **kwargs)

admin.site.register(JobFormField,JobFormAdmin)


class SupportPersonAdmin(ImportExportModelAdmin):
    list_display = ('name', 'contact_number', 'email')

    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="150" style="border-radius: 5px;" />'.format(obj.profile_picture.url))
        return "No Image"
    
    profile_picture_thumbnail.short_description = 'Profile Picture'

    readonly_fields = ['profile_picture_thumbnail']

admin.site.register(SupportPerson,SupportPersonAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('user', 'message')

    inlines = [ContactUsImageInline]

admin.site.register(ContactUs,ContactUsAdmin)

class ContactUsImageAdmin(admin.ModelAdmin):
    list_display = ('contact_us', 'created_at', 'updated_at')

admin.site.register(ContactUsImage,ContactUsImageAdmin)