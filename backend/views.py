from django.shortcuts import redirect
from backend.models import FaceSpaceUser, Friendship, Photo, Ad, Status
from backend.forms import PhotoForm, StatusForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from stronghold.decorators import public
from datetime import date


def upload(request):
    # todo: add validation
    form = PhotoForm(request.POST, request.FILES)

    if form.is_valid():
        picture = form.save(commit=False)
        picture.user = request.user
        picture.save()
        request.user.profile_picture = picture
        request.user.save()
    return redirect('profile', request.user.username)


def post_status(request):
    form = StatusForm(request.POST)

    if form.is_valid():
        status = form.save(commit=False)
        status.user = request.user
        status.save()
    return redirect('profile', request.user.username)


def upload_ad_pic(request):
    # @sam: use the form validator
    ad = Ad(content_photo=request.FILES['photo'], owner=request.user)
    ad.save()
    return redirect('profile', request.user.username)


def friend(request, other_friend_id):
    other_friend = FaceSpaceUser.objects.get(id=other_friend_id)
    Friendship.objects.create(to_friend=other_friend, from_friend=request.user)
    messages.success(request, "Sent friend request to {0}.".format(other_friend.get_full_name()))
    return redirect('profile', other_friend.username)


def confirm(request, friendship_id):
    friendship = Friendship.objects.get(id=friendship_id)
    friendship.confirmed = True
    friendship.save()
    messages.success(request, "Confirmed friendship with {0}".format(
        friendship.from_friend.get_full_name()))
    return redirect('profile', request.user.username)


def confirm_username(request, username):
    friendship = Friendship.objects.get(to_friend=request.user, from_friend__username=username)
    friendship.confirmed = True
    friendship.save()
    messages.success(request, "Confirmed friendship with {0}".format(
        friendship.from_friend.get_full_name()))
    return redirect('profile', request.user.username)


@public
def register(request):
    # todo: add form validation
    birthday = date(year=int(request.POST['birthday_year']),
                    month=int(request.POST['birthday_month']),
                    day=int(request.POST['birthday_day']))
    user = FaceSpaceUser.objects.create_user(username=request.POST['username'],
                                             password=request.POST['password'],
                                             email=request.POST['email'],
                                             birthday=birthday,
                                             is_male=bool(int(request.POST['sex'])),
                                             first_name=request.POST['firstname'],
                                             last_name=request.POST['lastname'])

    auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
    login(request, auth_user)
    return redirect('index')
