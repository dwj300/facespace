from django.db import models
from django.contrib.auth.models import AbstractUser


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)


class Entities(models.Model):
	time_created = models.DateTimeField()


class Likes(models.Model):
	pass


class Comments(models.Model):
	pass
