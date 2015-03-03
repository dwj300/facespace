from django.db import models
from django.contrib.auth.models import AbstractUser


class Comment(models.Model):
    user_id = models.ForeignKey('FaceSpaceUser')
    entity_id = models.OneToOneField('Entity')
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Entity(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('FaceSpaceUser')

    class Meta:
        verbose_name_plural = 'Entities'


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)
    relationship_with = models.ManyToManyField("self", through='Romance', symmetrical=False, related_name='relationship')
    friends_with = models.ManyToManyField("self", through='Friendship', symmetrical=False, related_name='friend')
    profile_picture = models.ForeignKey('Photo')


class Like(models.Model):
    user_id = models.ForeignKey('FaceSpaceUser')
    entity_id = models.ForeignKey('Entity')
    is_positive = models.BooleanField()


class Photo(Entity):
    caption = models.CharField()
    file_name = models.CharField()


class Status(Entity):
    text = models.TextField()


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
        unique_together = ('from_partner', 'to_partner')


class Friendship(models.Model):
    from_friend = models.ForeignKey('FaceSpaceUser', related_name='from_friend')
    to_friend = models.ForeignKey('FaceSpaceUser', related_name='to_friend')
    since = models.DateField()

    class Meta:
        unique_together = ('from_friend', 'to_friend')


class AdSlot(models.Model):
    bid_time = models.DateTimeField()
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    interest = models.OneToOneField('Interest')
    holds = models.ForeignKey('Ad', related_name="holding_ad_slots")
    will_hold = models.ForeignKey('Ad', related_name="will_hold_ad_slots")


class Interest(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', related_name="children", null=True)


class Ad(models.Model):
    content_link = models.URLField()
    owner = models.ForeignKey('FaceSpaceUser', null=False)


class Like(models.Model):
    user_id = models.ForeignKey('FaceSpaceUser')
    entity_id = models.ForeignKey('Entity')
    is_positive = models.BooleanField()
