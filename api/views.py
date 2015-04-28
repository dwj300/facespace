import json
from django.http import HttpResponse
from backend.models import Comment


def api(request):

	print 'hiiiii'
	if request.GET['action'] == 'comment_list':
		return comment_list(request)
	elif request.GET['action'] == 'like_list':
		return like_list(request)
	elif request.GET['action'] == 'like_entity':
		return like_entity(request)
	elif request.GET['action'] == 'post_comment':
		return post_comment(request)


def comment_list(request):
	response = {}
	entity_id = int(request.GET['entity_id'])

	c = Comment.objects.filter(entity=entity_id).order_by('time_created')

	response = {'code': 200,
	            'comments': c,
	           }

	return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))

def like_list(request):
	response = {}
	entity_id = int(request.GET['entity_id'])

	l = Like.objects.filter(entity=entity_id).filter(is_positive=True)
	d = Like.objects.filter(entity=entity_id).filter(is_positive=False)

	response = {'code': 200,
	            'likes': l,
	            'dislikes': d,
	           }

	return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
	
def like_entity(request):
	response = {}
	entity_id = int(request.GET['entity_id'])
	is_pos = int(request.GET['is_positive'])

	# todo: check if already liked

	l = Like.objects.create(entity=entity_id, 
		                    is_positive=is_pos, 
		                    user=request.user)

	response = {'code': 200,
	            'like': l,
	           }

	return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
	
def post_comment(request):
	response = {}
	entity_id = int(request.GET['entity_id'])
	text = request.GET['text']

	c = Comment.objects.create(entity=entity_id, 
		                       text=text, 
		                       user=request.user)

	response = {'code': 200,
	            'comment': c,
	           }

	return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
