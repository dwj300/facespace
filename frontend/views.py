from django.shortcuts import render
from stronghold.decorators import public
from backend.models import FaceSpaceUser, Interest
from django.db.models import Q


@public
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        return render(request, 'index.html')


def profile(request, username):
    if request.user.username == username:
        # getting your own profile
        pass
    else:
        # getting someone else's profile
        pass

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


def search(request):
    query = request.GET['query']
    terms = query.split(' ')
    people = FaceSpaceUser.objects.all()
    for term in terms:
        people = people.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))

    params = {'results': people}

    return render(request, 'search.html', params)
