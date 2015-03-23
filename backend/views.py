from django.shortcuts import render, redirect
from backend.models import Photo

# Create your views here.

def upload(request):
	print request.FILES
	# todo: add validation
	photo = Photo.objects.create(caption="foo", image=request.FILES["photo"], user=request.user)
	request.user.profile_picture = photo
	request.user.save()
	return redirect('profile', request.user.username)