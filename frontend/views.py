from django.shortcuts import render
from stronghold.decorators import public
from backend.models import FaceSpaceUser, Friendship, Interest
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


@public
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
    else:
        return render(request, 'index.html', {'day_list': range(1,32, 1),'year_list': range(2015, 1900, -1)})


def profile(request, username):
    params = {}
    try:
        other_user = FaceSpaceUser.objects.get(username=username)
        params['facespaceuser'] = other_user
    except ObjectDoesNotExist:
        # user doesnt exist
        # redirect to homepage
        pass

    if other_user == request.user:
        # getting your own profile
        pending_friends = Friendship.objects.filter(to_friend=request.user, confirmed=False).values('from_friend__first_name', 'id')
        confirmed_friends = Friendship.objects.filter(Q(to_friend=request.user)|Q(from_friend=request.user), confirmed=True)
        params['pending_friends'] = list(pending_friends)
        params['confirmed_friends'] = list(confirmed_friends)
        return render(request, 'profile.html', params)
    elif Friendship.objects.filter((Q(to_friend=request.user)   & Q(from_friend=other_user)) | \
                                   (Q(from_friend=request.user) & Q(to_friend=other_user)),
                                   confirmed=True).count() == 1:
        # getting a friend's profile
        return render(request, 'profile_friend.html', params)
    else:
        # getting someone else's profile
        try:
            friendship = Friendship.objects.get((Q(to_friend=request.user) & Q(from_friend=other_user)) | (Q(from_friend=request.user) & Q(to_friend=other_user)), confirmed=False)
            params['friendship'] = friendship
        except:
            pass
        return render(request, 'profile_other.html', params)

    
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
