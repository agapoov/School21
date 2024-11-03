from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    surname = models.CharField(max_length=128)
    tg_username = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
