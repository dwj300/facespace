from django.db import models
from django.contrib.auth.models import AbstractUser


class Comment(models.Model):
	user_id = models.ForeignKey('FaceSpaceUser')
	entity_id = models.ForeignKey('Entity')
	time_created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()


class Entity(models.Model):
	time_created = models.DateTimeField(auto_now_add=True)


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)


class Like(models.Model):
	user_id = models.ForeignKey('FaceSpaceUser')
	entity_id = models.ForeignKey('Entity')
	is_positive = models.BooleanField()