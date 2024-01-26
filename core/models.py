from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_service_provider = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"