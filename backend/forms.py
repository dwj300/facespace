from django.forms import ModelForm, Form, DecimalField, ModelChoiceField
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

    def __init__(self, user, init_price, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['price'].initial = init_price
        self.fields['ad'].queryset = Ad.objects.filter(owner=user)

    price = DecimalField(max_digits=9, decimal_places=2)
    ad = ModelChoiceField(queryset=None,empty_label=None)


class StatusForm(ModelForm):

    class Meta:
        model = Status
        exclude = ['user']
