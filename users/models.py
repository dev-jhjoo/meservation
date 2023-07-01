from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    short_description = models.TextField("설명", blank=True)

    def __str__(self):
        return self.username
  