from django.forms import ModelForm, CharField, TextInput
from backend.models import Photo


class PhotoForm(ModelForm):
    caption = CharField(widget=TextInput)

    class Meta:
        model = Photo
        exclude = ['user']
