from django.db import models
from django.contrib.auth.models import AbstractUser


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)

