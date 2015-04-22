from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class Interest(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', related_name="children", null=True, blank=True)
    bid_time = models.DateTimeField(null=True, blank=True)
    bid_price = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0.99)
    holds = models.ForeignKey('Ad', related_name='holding_ad_slots', null=True, blank=True)
    will_hold = models.ForeignKey('Ad', related_name='will_hold_ad_slots', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'interests'


class Ad(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    content_photo = models.ImageField(upload_to="ads")
    owner = models.ForeignKey('FaceSpaceUser', null=False)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        db_table = 'ads'


class Comment(models.Model):
    user = models.ForeignKey('FaceSpaceUser', null=False)
    entity = models.ForeignKey('Entity')
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        db_table = 'comments'


class Entity(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('FaceSpaceUser')

    class Meta:
        verbose_name_plural = 'Entities'
        db_table = 'entities'


class FaceSpaceUser(AbstractUser):
    birthday = models.DateField()
    is_male = models.BooleanField(default=True)
    profile_picture = models.ForeignKey('Photo', null=True, blank=True)
    relationship_with = models.ManyToManyField(
        "self", through='Romance', symmetrical=False, related_name='relationship')
    friends = models.ManyToManyField(
        "self", through='Friendship', symmetrical=False, related_name='friend')
    interests = models.ManyToManyField('Interest', blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birthday', 'is_male']

    @property
    def pending_friendships(self):
        return Friendship.objects.filter(to_friend=self, confirmed=False)

    @property
    def pending_friends(self):
        return map(lambda x: x['from_friend'], Friendship.objects.filter(to_friend=self, confirmed=False).values('from_friend'))

    @property
    def pending_other_friends(self):
        return map(lambda x: x['to_friend'], Friendship.objects.filter(from_friend=self, confirmed=False).values('to_friend'))

    @property
    def confirmed_friends(self):
        confirmed_friendships = Friendship.objects.filter(Q(to_friend=self) | Q(from_friend=self), confirmed=True)
        friends = []
        for friendship in confirmed_friendships:
            if friendship.to_friend == self:
                friends.append(friendship.from_friend)
            else:
                friends.append(friendship.to_friend)
        return friends

    @property
    def pending_romances(self):
        return Romance.objects.filter(to_partner=self,confirmed=False)

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'facespaceusers'


class Friendship(models.Model):
    from_friend = models.ForeignKey('FaceSpaceUser', related_name='from_friend')
    to_friend = models.ForeignKey('FaceSpaceUser', related_name='to_friend')
    since = models.DateField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        if self.confirmed:
            return " ".join([str(self.from_friend), "<->", str(self.to_friend)])
        else:
            return "{0} -> {1}".format(str(self.from_friend), str(self.to_friend))

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

    def __unicode__(self):
        return "{0} likes {1}".format(str(self.user), str(self.entity))


class Photo(Entity):
    caption = models.CharField(max_length=140)
    image = models.ImageField(upload_to="photos")

    def __unicode__(self):
        return self.caption[:10]

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
    romance_type = models.CharField(max_length=10, choices=ROMANCE_TYPES, default=DATING)
    since = models.DateField()
    until = models.DateField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return " ".join([str(self.from_partner), "<3", str(self.to_partner)])

    class Meta:
        db_table = 'romances'
        unique_together = ('from_partner', 'to_partner', 'since')


class Status(Entity):
    text = models.CharField(max_length=140)

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        db_table = 'statuses'
        verbose_name_plural = 'statuses'
