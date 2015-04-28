import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from backend.models import Comment, Like, Status


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

    print 'well thats not good'


def newsfeed_list(request):
    response = {}

    friends = request.user.confirmed_friends
    friends.append(request.user)
    statuses = Status.objects.filter(user__in=friends).order_by('-time_created')

    ps = statuses
    posts = []

    for p in ps:
        post = {}
        post['user_id'] = p.user.id
        post['user_name'] = p.user.username
        post['age'] = '22 mins'
        post['text'] = p.text

        likes = []

        for l in Like.objects.filter(entity=p.id).filter(is_positive=True):
            likes.append({'user_name': l.user.username,
                          'user_id': l.user.id
                         })
        post['likes'] = likes

        dislikes = []

        for l in Like.objects.filter(entity=p.id).filter(is_positive=False):
            dislikes.append({'user_name': l.user.username,
                             'user_id': l.user.id
                            })
        post['dislikes'] = dislikes

        comments = []

        for c in Comment.objects.filter(entity=p.id).order_by('time_created'):
            comments.append({'user_name': c.user.username,
                             'user_id': c.user.id,
                             'text': c.text,
                             'age': '5 days'
                            })


        posts.append(post)

    response = {'code': 200,
                'posts': posts,
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
