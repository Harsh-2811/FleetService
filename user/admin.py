from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomeUserAdmin(UserAdmin):
    pass

admin.site.register(User,CustomeUserAdmin)