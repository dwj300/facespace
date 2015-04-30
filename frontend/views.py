from django.shortcuts import render, redirect
from stronghold.decorators import public
from backend.models import Ad, FaceSpaceUser, Status
from backend.models import Friendship, Interest, Romance
from backend.forms import PhotoForm, InterestForm, AdForm, BidForm, StatusForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from django.http import HttpResponse


@public
def index(request):
    if request.user.is_authenticated():
        return newsfeed(request)
    else:
        return render(request,
                      'index.html',
                      {'day_list': range(1, 32, 1), 'year_list': range(2015, 1900, -1)})


def about(request):
    return render(request, 'about.html')


def newsfeed(request):
    params = {}

    # get stuff
    # todo: filter only friends' content
    friends = request.user.confirmed_friends
    friends.append(request.user)
    statuses = Status.objects.all().filter(user__in=friends).order_by('-time_created')
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
        params['statuses'] = Status.objects.filter(user=request.user).order_by('-time_created')
        params['photo_form'] = PhotoForm()
        params['status_form'] = StatusForm()
        return render(request, 'profile.html', params)
    
    elif Friendship.objects.filter((Q(to_friend=request.user) & Q(from_friend=other_user)) |
                                   (Q(from_friend=request.user) & Q(to_friend=other_user)),
                                   confirmed=True).count() == 1:
        # getting a friend's profile
        params['statuses'] = Status.objects.filter(user=other_user)
        

        romances = Romance.objects.filter(
            (Q(to_partner=request.user) & Q(from_partner=other_user)) | 
            (Q(from_partner=request.user) & Q(to_partner=other_user)))

        cur_romance = [r for r in romances if r.confirmed == True]
        if cur_romance:
            if cur_romance[0].romance_type == Romance.DATING:
                params['next_romance'] = 'Propose'
                params['next_breakup'] = 'Breakup'
            elif cur_romance[0].romance_type == Romance.ENGAGED:
                params['next_romance'] = 'Get Married!'
                params['next_breakup'] = 'Break it off'
            else:
                params['next_romance'] = ''
                params['next_breakup'] = 'Get divorced!'

            print cur_romance[0], cur_romance[0].confirmed

        else:
            params['next_romance'] = 'Go Steady'
            params['next_breakup'] = ''

        requested_romance = [r for r in romances if r.confirmed == False]
        if requested_romance:
            if r.from_partner == request.user:
                params['romance_request'] = 'Romance Request Sent'
            else:
                params['romance_request'] = ' '



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

    interest = Interest.objects.get(id=interest_id)

    if request.POST:
        price = float(request.POST.get('price'))
        ad_id = request.POST.get('ad')
        if interest.bid_price < price:
            interest.will_hold = Ad.objects.get(id=ad_id)
            interest.bid_price = price
            interest.bid_time = datetime.now()
            interest.save()
            return redirect('interest', interest_id)

    form = BidForm(user=request.user, init_price=interest.bid_price)
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
    #todo: interests search
    params = {}
    query = request.GET['query']
    terms = query.split(' ')
    people = FaceSpaceUser.objects.all()
    posts = Status.objects.all()
    interests = Interest.objects.all()
    for term in terms:
        people = people.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        posts = posts.filter(text__icontains=term)
        interests = interests.filter(name__icontains=term)

    params['user_results'] = people
    params['status_results'] = posts
    params['interest_results'] = interests
#

    params['keyword'] = query

    return render(request, 'search.html', params)


class UserChatView(TemplateView):
    template_name = 'user_chat.html'

    def get_context_data(self, **kwargs):
        context = super(UserChatView, self).get_context_data(**kwargs)
        context.update(users=FaceSpaceUser.objects.all())
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserChatView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='foobar', users=[request.POST.get('user')])
        message = RedisMessage(request.POST.get('message'))
        redis_publisher.publish_message(message)
        return HttpResponse('OK')
