from django.shortcuts import render, redirect
from stronghold.decorators import public
from backend.models import Ad, Comment, FaceSpaceUser, Romance, Status
from backend.models import Friendship, Interest, Like, Photo
from backend.forms import PhotoForm, InterestForm, AdForm, BidForm, StatusForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


@public
def index(request):
    if request.user.is_authenticated():
        return newsfeed(request)
    else:
        return render(request,
                      'index.html',
                      {'day_list': range(1, 32, 1), 'year_list': range(2015, 1900, -1)})


def newsfeed(request):
    params = {}

    # get stuff
    # todo: filter only friends' content
    statuses = Status.objects.all()
    # likes = Like.objects.all()
    # comments = Comment.objects.all()
    # friendships = Friendship.objects.all()
    # photos = Photo.objects.all()
    # romance = Romance.objects.all()

    params['statuses'] = statuses
    params['user'] = request.user

    return render(request, 'home.html', params)


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
        # confirmed_friends = Friendship.objects.filter(Q(to_friend=request.user)|Q(from_friend=request.user), confirmed=True)
        # params['confirmed_friends'] = list(confirmed_friends)
        params['statuses'] = Status.objects.filter(user=request.user)
        params['photo_form'] = PhotoForm()
        params['status_form'] = StatusForm()
        return render(request, 'profile.html', params)
    elif Friendship.objects.filter((Q(to_friend=request.user) & Q(from_friend=other_user)) |
                                   (Q(from_friend=request.user) & Q(to_friend=other_user)),
                                   confirmed=True).count() == 1:
        # getting a friend's profile
        return render(request, 'profile_friend.html', params)
    else:
        # getting someone else's profile
        try:
            friendship = Friendship.objects.get((Q(to_friend=request.user) & Q(from_friend=other_user)) | (
                Q(from_friend=request.user) & Q(to_friend=other_user)), confirmed=False)
            params['friendship'] = friendship
        except:
            pass
        return render(request, 'profile_other.html', params)


def bid(request, interest_id):
    form = BidForm()
    interest = Interest.objects.get(id=interest_id)
    params = {'form': form, 'interest': interest}
    return render(request, 'bid.html', params)


def create_ad(request):
    if request.POST:
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect('interest', 1)
        else:
            return redirect('create_ad')
    else:
        form = AdForm()
        params = {'form': form}
        return render(request, 'create_ad.html', params)


def create_interest(request):
    if request.POST:
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=True)
            return redirect('interest', interest.id)
        else:
            return redirect('create_interest')
    else:
        form = InterestForm()
        params = {'form': form}
        return render(request, 'create_interest.html', params)


def interest(request, interest_id):
    params = {}
    try:
        interest = Interest.objects.get(id=interest_id)

        child_interests = Interest.objects.filter(parent__id=interest_id)

        params['child_interests'] = child_interests

        if not interest.holds:
            print "asdfadsfadfs"
            ad = Ad.objects.get(id=1)
            print ad.name
            interest.holds = ad
            interest.save()

        params['interest'] = interest
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
