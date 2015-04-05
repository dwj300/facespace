from django.forms import ModelForm, Form, DecimalField
from backend.models import Status, Photo, Interest, Ad


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = ['user']


class InterestForm(ModelForm):

    class Meta:
        model = Interest
        exclude = ['bid_time', 'bid_price', 'holds', 'will_hold']


class AdForm(ModelForm):

    class Meta:
        model = Ad
        exclude = ['owner']


class BidForm(Form):
    price = DecimalField(max_digits=9, decimal_places=2)


class StatusForm(ModelForm):

    class Meta:
        model = Status
        exclude = ['user']
