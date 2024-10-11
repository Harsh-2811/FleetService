from django.db import models
from django.contrib.auth.models import AbstractUser,Group

# Create your models here.
class User(AbstractUser):
    is_driver=models.BooleanField(default=True)


    def __str__(self):
<<<<<<< HEAD
        return f"{self.username}-{self.first_name}"
=======
        return self.username
>>>>>>> 6f6d7cd023491d6a39f4b3d4203f41e8d853486a
