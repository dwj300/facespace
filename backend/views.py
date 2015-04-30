from django.shortcuts import redirect
from backend.models import FaceSpaceUser, Friendship, Ad, Romance
from django.db.models import Q
from backend.forms import PhotoForm, StatusForm
from django.contrib import messages
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


def romance_up(request, other_partner_id):
    """Create an unconfirmed Romance between request.user and other_partner"""

    partner = FaceSpaceUser.objects.get(id=other_partner_id)
    try:
        romance = Romance.objects.get((Q(to_partner=partner) & Q(from_partner=request.user)) | 
                                      (Q(from_partner=partner) & Q(to_partner=request.user)))
        
        if romance.romance_type == Romance.DATING:
            Romance.objects.create(to_partner=partner, 
                                   from_partner=request.user, 
                                   since=date.today(), 
                                   romance_type=Romance.ENGAGED)

        elif romance.romance_type == Romance.ENGAGED:
            Romance.objects.create(to_partner=partner, 
                                   from_partner=request.user, 
                                   since=date.today(), 
                                   romance_type=Romance.MARRIED)
    except:
        Romance.objects.create(to_partner=partner, 
                               from_partner=request.user, 
                               since=date.today())
    
    messages.success(request, "Sent romance request to {0}.".format(partner.get_full_name()))
    return redirect('profile', partner.username)


def romance_down(request, other_partner_id):
    """Delete all romances between request.user and other_partner_id"""

    partner = FaceSpaceUser.objects.get(id=other_partner_id)
    romances = Romance.objects.filter((Q(to_partner=partner) & Q(from_partner=request.user)) | 
                                      (Q(from_partner=partner) & Q(to_partner=request.user)))
    [r.delete() for r in romances]
    return redirect('profile', partner.username)


def confirm(request, friendship_id):
    friendship = Friendship.objects.get(id=friendship_id)
    friendship.confirmed = True
    friendship.save()
    messages.success(request, "Confirmed friendship with {0}"
        .format(friendship.from_friend.get_full_name()))
    return redirect('profile', request.user.username)


def confirm_romance(request, romance_id, confirmed):
    """if confirmed, confirm romance and delete any lesser romances. Else, delete this romance"""

    romance = Romance.objects.get(id=romance_id)
    if confirmed == '1':
        romance.confirmed = True
        romance.save()
        p1 = romance.from_partner
        p2 = romance.to_partner
        if romance.romance_type == Romance.ENGAGED:
            prev_romance = Romance.objects.get(Q(romance_type=Romance.DATING) & 
                                            ((Q(to_partner=p1) & Q(from_partner=p2)) | 
                                             (Q(from_partner=p1) & Q(to_partner=p2))))
            prev_romance.delete()
        
        if romance.romance_type == Romance.MARRIED:
            prev_romance = Romance.objects.get(Q(romance_type=Romance.ENGAGED) & 
                                            ((Q(to_partner=p1) & Q(from_partner=p2)) | 
                                             (Q(from_partner=p1) & Q(to_partner=p2))))
            prev_romance.delete()
            

        messages.success(request, "Confirmed romance with {0}"  
            .format(romance.from_partner.get_full_name()))

    else:
        romance.delete()
        messages.success(request, "Denied romance!")
    
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
    FaceSpaceUser.objects.create_user(username=request.POST['username'],
                                      password=request.POST['password'],
                                      email=request.POST['email'],
                                      birthday=birthday,
                                      is_male=bool(int(request.POST['sex'])),
                                      first_name=request.POST['firstname'],
                                      last_name=request.POST['lastname'])

    auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
    login(request, auth_user)
    return redirect('index')
