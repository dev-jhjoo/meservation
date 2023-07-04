import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    short_description = models.TextField(blank=True, verbose_name="한 줄 소개")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID")

    def __str__(self):
        return self.username
  