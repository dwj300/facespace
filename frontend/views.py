from django.shortcuts import render
from stronghold.decorators import public
from backend.models import FaceSpaceUser, Interest

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

def interest(request, interest_id):
    params = {}
    try:
        interest = Interest.objects.get(id=interest_id)
        params['interest'] = interest
        child_interests = Interest.objects.filter(parent__id=interest_id)
        params['child_interests'] = child_interests
    except:
        pass

    return render(request, 'interest.html', params)