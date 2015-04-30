from itertools import chain
import json
from operator import attrgetter

from datetime import timedelta

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import timezone

from sorl.thumbnail import get_thumbnail

from backend.models import Comment, Like, Status, FaceSpaceUser, Photo


def api(request):
    print 'api land'
    if 'action' in request.GET:
        if request.GET['action'] == 'comment_list':
            return comment_list(request)
        elif request.GET['action'] == 'like_list':
            return like_list(request)
        elif request.GET['action'] == 'like_entity':
            return like_entity(request)
        elif request.GET['action'] == 'unlike_entity':
            return unlike_entity(request)
        elif request.GET['action'] == 'post_comment':
            return post_comment(request)
        elif request.GET['action'] == 'newsfeed_list':
            return newsfeed_list(request)
        elif request.GET['action'] == 'get_thumbnail_url':
            return get_thumbnail_url(request)

    print 'well thats not good'


def get_thumbnail_url(request):
    response = {}

    dim = int(request.GET['dim'])
    user_id = int(request.GET['user_id'])

    user = FaceSpaceUser.objects.get(id=user_id)

    im = get_thumbnail(user.profile_picture.image, 
                       str(dim) + 'x' + str(dim), 
                       crop='center')

    response = {'code': 200,
                'im_url': im.url,
                'message': 'URLED!'
               }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))


def calc_age(time_created):
    delta = timezone.now() - time_created

    if delta < timedelta(minutes=1):
        return 'now'
    elif delta < timedelta(hours=1):
        mins = delta.seconds/60
        return str(mins) + ' mins' if mins > 1 else ' min'
    elif delta < timedelta(days=1):
        hrs = delta.seconds/3600
        return str(hrs) + ' hrs' if hrs > 1 else ' hr'
    else:
        print delta.days
        return str(delta.days) + (' days' if delta.days > 1 else ' day')


def newsfeed_list(request):
    response = {}

    friends = request.user.confirmed_friends
    friends.append(request.user)
    statuses = Status.objects.filter(user__in=friends).order_by('-time_created')
    photos = Photo.objects.filter(user__in=friends).order_by('-time_created')

    ps = sorted(chain(statuses, photos), key=attrgetter('time_created'), reverse=True)

    print ps

    posts = []

    for p in ps:
        post = {}
        if type(p) is Photo:
            post['type'] = 'Photo'
            post['text'] = p.caption
            post['photo_url'] = get_thumbnail(p.image, "500x500").url
        else:
            post['type'] = 'Status'
            post['text'] = p.text
        
        post['post_id'] = p.id
        post['user_id'] = p.user.id
        post['user_name'] = p.user.username
        post['full_name'] = p.user.get_full_name()
        post['age'] = calc_age(p.time_created)
        post['liked'] = Like.objects.filter(entity=p.id
                                   ).filter(user=request.user
                                   ).filter(is_positive=True).exists()
        post['disliked'] = Like.objects.filter(entity=p.id
                                      ).filter(user=request.user
                                      ).filter(is_positive=False).exists()

        user = FaceSpaceUser.objects.get(id=p.user.id)
        im40 = get_thumbnail(user.profile_picture.image, '40x40', crop='center')
        post['im_url'] = im40.url

        likes = []

        for l in Like.objects.filter(entity=p.id).filter(is_positive=True):
            likes.append({'user_name': l.user.username,
                          'user_full_name': l.user.get_full_name(),
                          'user_id': l.user.id
                         })
        post['likes'] = likes

        dislikes = []

        for l in Like.objects.filter(entity=p.id).filter(is_positive=False):
            dislikes.append({'user_name': l.user.username,
                             'user_full_name': l.user.get_full_name(),
                             'user_id': l.user.id
                            })
        post['dislikes'] = dislikes

        comments = []

        for c in Comment.objects.filter(entity=p.id).order_by('time_created'):
            user = FaceSpaceUser.objects.get(id=c.user.id)

            im40 = get_thumbnail(user.profile_picture.image, '40x40', crop='center')

            comments.append({'user_name': c.user.username,
                             'user_id': c.user.id,
                             'user_full_name': c.user.get_full_name(),
                             'text': c.text,
                             'age': calc_age(c.time_created),
                             'im_url': im40.url
                            })

        post['comments'] = comments
        posts.append(post)


    user = FaceSpaceUser.objects.get(id=request.user.id)
    im32 = get_thumbnail(user.profile_picture.image, '32x32', crop='center')

    response = {'code': 200,
                'posts': posts,
                'im_url': im32.url
               }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))

def comment_list(request):
    response = {}
    entity_id = int(request.GET['entity_id'])

    c = Comment.objects.filter(entity=entity_id).order_by('time_created')

    response = {'code': 200,
                'comments': c,
               }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))

def like_list(request):
    print 'like list land'
    response = {}
    entity_id = int(request.GET['entity_id'])

    likes = []

    for l in Like.objects.filter(entity=entity_id).filter(is_positive=True):
        likes.append({'user_id': l.user.username,
                      'user_name': l.user.id
                     })
    dislikes = []

    for d in Like.objects.filter(entity=entity_id).filter(is_positive=False):
        dislikes.append({'user_id': d.user.username,
                         'user_name': d.user.id
                        })

    response = {'code': 200,
                'likes': likes,
                'dislikes': dislikes,
               }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
    
def like_entity(request):
    response = {}
    entity_id = int(request.GET['entity_id'])
    is_pos = int(request.GET['is_positive'])

    if Like.objects.filter(entity=entity_id
                  ).filter(user=request.user
                  ).filter(is_positive=is_pos).exists():
        response = {'code': 200,
                    'success': False,
                    'entity_id': entity_id,
                    'message': '{} already {}liked this entity.'.format(
                                    request.user.username,
                                    '' if is_pos == 1 else 'dis')}  

    else:
        Like.objects.filter(entity=entity_id
                   ).filter(user=request.user
                   ).exclude(is_positive=is_pos).delete()

        Like.objects.create(entity_id=entity_id, 
                            is_positive=is_pos, 
                            user=request.user)

        response = {'code': 200,
                    'success': True,
                    'entity_id': entity_id,
                    'message': '{} {}liked this entity!'.format(
                                    request.user.username,
                                    '' if is_pos == 1 else 'dis')}

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))

def unlike_entity(request):
    response = {}
    entity_id = int(request.GET['entity_id'])
    is_pos = int(request.GET['is_positive'])

    if Like.objects.filter(entity=entity_id
                  ).filter(user=request.user
                  ).filter(is_positive=is_pos).exists():
        Like.objects.filter(entity=entity_id
                   ).filter(user=request.user
                   ).filter(is_positive=is_pos).delete()

        response = {'code': 200,
                    'success': True,
                    'entity_id': entity_id,
                    'message': '{} un{}liked this entity!'.format(
                                    request.user.username,
                                    '' if is_pos == 1 else 'dis'),
                   }    

    else:
        response = {'code': 200,
                    'success': False,
                    'entity_id': entity_id,
                    'message': '{} hasn\'t {}liked this entity.'.format(
                                    request.user.username,
                                    '' if is_pos == 1 else 'dis')}  

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
    
def post_comment(request):
    response = {}
    if 'entity_id' in request.GET and 'text' in request.GET:
        entity_id = int(request.GET['entity_id'])
        text = request.GET['text']

        c = Comment.objects.create(entity_id=entity_id, 
                                   text=text, 
                                   user=request.user)

        response = {'code': 200,
                    'success': True,
                    'message': '{} posted a comment!'.format(request.user.username)
                   }
    else:
        response = {'code': 200,
                    'success': False,
                    'message': 'entity_id and text must be specified'
                   }

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
