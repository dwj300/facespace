from django.shortcuts import redirect  # , render
from backend.models import Photo


def upload(request):
    # todo: add validation
    photo = Photo.objects.create(caption="foo",
                                 image=request.FILES["photo"],
                                 user=request.user)
    request.user.profile_picture = photo
    request.user.save()
    return redirect('profile', request.user.username)
