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
    relationship_with = models.ManyToManyField("self", through='Romance', symmetrical=False, related_name='relationship')
    friends_with = models.ManyToManyField("self", through='Friendship', symmetrical=False, related_name='friend')


class Romance(models.Model):
    DATING = 'Dating'
    ENGAGED = 'Engaged'
    MARRIED = 'Married'
    ROMANCE_TYPES = (
        (DATING, 'Dating'),
        (ENGAGED, 'Engaged'),
        (MARRIED, 'Married'),
    )
    from_partner = models.ForeignKey('FaceSpaceUser', related_name='from_partner')
    to_partner = models.ForeignKey('FaceSpaceUser', related_name='to_partner')
    romance_type = models.CharField(max_length=10, choices = ROMANCE_TYPES, default=DATING)
    since = models.DateField()

    class Meta:
        unique_together = ('from_partner','to_partner')


class Friendship(models.Model):
    from_friend = models.ForeignKey('FaceSpaceUser', related_name='from_friend')
    to_friend = models.ForeignKey('FaceSpaceUser', related_name='to_friend')
    since = models.DateField()

    class Meta:
        unique_together = ('from_friend','to_friend')


class Like(models.Model):
	user_id = models.ForeignKey('FaceSpaceUser')
	entity_id = models.ForeignKey('Entity')
	is_positive = models.BooleanField()
