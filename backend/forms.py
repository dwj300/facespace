from django.forms import ModelForm
from backend.models import Photo


class PhotoForm(ModelForm):
	class Meta:
		model = Photo
		exclude = ['user']