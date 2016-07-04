from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from post.models import PostModel
from django.http import HttpResponse
# Create your views here.

def can_view_post(post, user):
	#Only the authors can view a post. Staff can only view submitted posts.
	return user.is_superuser\
	or\
	user.groups.filter(name='staff').exists() and post.status == 'post'\
	or\
	user in post.authors.all()

@login_required
def view_post(request, post_id):
	if not PostModel.objects.filter(id=post_id).exists():
		return HttpResponse("The post doesn't exist.")

	post = PostModel.objects.get(id=post_id)
	if not can_view_post(post,request.user):
		return HttpResponse ('Access denied.')
		
	context = {}
	context['post'] = post
	context.update(csrf(request))
	return render(request, 'post/post.html', context)
		