from django.shortcuts import render
from stronghold.decorators import public
from backend.models import FaceSpaceUser
from django.db.models import Q
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

def search(request):
    query = request.GET['query']
    terms = query.split(' ')
    people = FaceSpaceUser.objects.all()
    for term in terms:
        people = people.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))

    params = {'results': people}

    return render(request, 'search.html', params)