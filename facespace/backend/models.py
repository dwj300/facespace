from django.db import models
from django.contrib.auth.models import AbstractUser

class Interest(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', related_name="children", null=True)

    class Meta:
        db_table = 'interests'


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)
    profile_picture = models.ForeignKey('Photo', null=True)
    relationship_with = models.ManyToManyField("self", through='Romance', symmetrical=False, related_name='relationship')
    friends_with = models.ManyToManyField("self", through='Friendship', symmetrical=False, related_name='friend')
    interested_in = models.ManyToManyField('Interest')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birthday', 'is_male']

    class Meta:
        db_table = 'facespaceusers'


class Entity(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('FaceSpaceUser')

    class Meta:
        verbose_name_plural = 'Entities'
        db_table = 'entities'


class Ad(models.Model):
    content_link = models.URLField()
    owner = models.ForeignKey('FaceSpaceUser', null=False)

    class Meta:
        db_table = 'ads'


class AdSlot(models.Model):
    bid_time = models.DateTimeField()
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    interest = models.OneToOneField('Interest')
    holds = models.ForeignKey('Ad', related_name='holding_ad_slots')
    will_hold = models.ForeignKey('Ad', related_name='will_hold_ad_slots', null=True)

    class Meta:
        db_table = 'adslots'


class Comment(models.Model):
    user = models.ForeignKey('FaceSpaceUser', null=False)
    entity = models.ForeignKey('Entity')
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        db_table = 'comments'


class Friendship(models.Model):
    from_friend = models.ForeignKey('FaceSpaceUser', related_name='from_friend')
    to_friend = models.ForeignKey('FaceSpaceUser', related_name='to_friend')
    since = models.DateField()

    class Meta:
        unique_together = ('from_friend', 'to_friend')
        db_table = 'friendships'


class Like(models.Model):
    user = models.ForeignKey('FaceSpaceUser')
    entity = models.ForeignKey('Entity')
    is_positive = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'entity')
        db_table = 'likes'


class Photo(Entity):
    caption = models.TextField()
    file_name = models.CharField(max_length=75)

    class Meta:
        db_table = 'photos'


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
    until = models.DateField(null=True)

    class Meta:
        db_table = 'romances'
        unique_together = ('from_partner', 'to_partner', 'since')


class Status(Entity):
    text = models.TextField()

    class Meta:
        db_table = 'statuses'
