from django.shortcuts import render
from stronghold.decorators import public
from backend.models import FaceSpaceUser

# Create your views here.


@public
def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def profile(request, username):
    params = {}
    try:
        user = FaceSpaceUser.objects.get(username=username)
        params['facespaceuser'] = user
    except:
        # redirect to homepage
        pass

    return render(request, 'profile.html', params)
