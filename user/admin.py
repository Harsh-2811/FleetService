from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

# Register your models here.
class CustomeUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Driver Info", {'fields': ('is_driver', 'first_name', 'last_name')}),
    )

admin.site.register(User, CustomeUserAdmin)