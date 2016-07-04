from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from post.models import PostModel
from datetime import datetime
from django.http import HttpResponse
import json
# Create your views here.

def can_edit_post(post, user):
	#Only the owner can edit a draft. Staff can edit a post after submission.
	return user.groups.filter(name='staff').exists() and post.status == 'post'\
	or\
	user.is_superuser\
	or\
	user.id == post.owner.id and post.status == 'draft'

def can_delete_post(post, user):
	#Only the owner can delete a draft. Staff can edit a post after submission.
	return user.is_superuser\
	or\
	user.groups.filter(name='staff').exists() and user.id == post.owner.id\
	or\
	user.id == post.owner.id and post.status == 'draft'

@login_required
def post_editor(request, post_id):
	#Edit an existing post.
	if not PostModel.objects.filter(id=post_id).exists():
		return HttpResponse("The post doesn't exist.")
	post = PostModel.objects.get(id=post_id)
	if not can_edit_post(post, request.user):
		return HttpResponse('Access denied.')

	context = {}
	context.update(csrf(request))	
	context['title'] = post.title
	context['content'] = post.content
	context['post_id'] = post_id
	return render(request, 'editor/editor.html', context)

@login_required
def new_editor(request):
	#Start a new editor.
	context = {}
	context.update(csrf(request))
	return render(request, 'editor/editor.html', context)

@login_required
def save_draft(request):
	title = request.POST.get('title')
	content = request.POST.get('content')
	post_id = request.POST.get('post_id')
	if post_id:
		#If there is a record of the draft, update the record.
		if not PostModel.objects.filter(id=post_id).exists():
			return HttpResponse("The post doesn't exist.")
		post = PostModel.objects.get(id=post_id)
		if not can_edit_post(post, request.user):
			return HttpResponse('Access denied.')
		post.title = title
		post.content = content
		post.date_stamp = datetime.now()
		post.save()
	else:
		#If the draft has never been saved before, create a new instance.
		post = PostModel(title=title, content=content, date_stamp = datetime.now(), owner=request.user)
		post.status = 'draft'
		post.save()
		post.authors.add(request.user)
	
	#If a new instance was created, the client needs post.id for future savings.
	return HttpResponse(json.dumps({'post_id': post.id}), content_type='application/json')

@login_required
def submit(request):
	title = request.POST.get('title')
	content = request.POST.get('content')
	post_id = request.POST.get('post_id')
	if post_id:
		#If there is a record of the draft, update the record.
		if not PostModel.objects.filter(id=post_id).exists():
			return HttpResponse("The post doesn't exist.")
		post = PostModel.objects.get(id=post_id)
		if not can_edit_post(post, request.user):
			return HttpResponse('Access denied.')
		post.title = title
		post.content = content
		post.date_stamp = datetime.now()
		post.status = 'post'
		post.save()
	else:
		#If the draft has never been saved before, create a new instance.
		post = PostModel(title=title, content=content, date_stamp = datetime.now(), owner=request.user)
		post.status = 'post'
		post.save()
		post.authors.add(request.user)

	return redirect('/accounts/profile/')

@login_required
def delete(request, post_id):
	if post_id:
		#If there is a record of the draft, update the record.
		if not PostModel.objects.filter(id=post_id).exists():
			return HttpResponse("The post doesn't exist.")
		post = PostModel.objects.get(id=post_id)
		if not can_delete_post(post, request.user):
			return HttpResponse('Access denied.')
		post.delete()
	else:
		return HttpResponse('Post ID not specified.')

	return redirect('/accounts/profile/')