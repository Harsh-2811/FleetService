from django.db import models
from django.contrib.auth.models import AbstractUser,Group

# Create your models here.
class User(AbstractUser):
    is_driver=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}-{self.first_name}"
