from django.db import models
from django.contrib.auth.models import AbstractUser


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)


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