from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from post.models import PostModel, CommentModel
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime
import json
# Create your views here.

def can_view_post(post, user):
	#Only the authors can view a post. Staff can only view submitted posts.
	return user.is_superuser\
	or\
	user.groups.filter(name='staff').exists() and post.status == 'post'\
	or\
	user in post.authors.all()

def comments_filter(user, comments):
	#Select out the comments that can be accessed by the user.
	return [comment for comment in comments\
	if comment.scope == 'public'\
	or comment.commenter.id == user.id\
	or (comment.reply_to and comment.reply_to.id == user.id)\
	or (comment.parent_post and comment.parent_post.owner.id == user.id)\
	or (not comment.reply_to and comment.parent_comment and comment.parent_comment.commenter.id == user.id)]


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

	comments_list = []
	comments = comments_filter(request.user, post.comments.all())
	for comment in comments:
		child_comments = comments_filter(request.user, comment.child_comments.all())
		comments_list.append({'comment':comment, 'child_comments':child_comments})
	context['comments_list'] = comments_list

	return render(request, 'post/post.html', context)

def save_comment(request):
	content = request.POST.get('content','')

	#Update an existing comment
	comment_id = request.POST.get('comment_id','')
	if comment_id:
		if not CommentModel.objects.filter(id=comment_id).exists():
			return HttpResponse(jason.dumps({error:"The comment dosen't exist."}), content_type='application/json')
		comment = CommentModel.objects.get(id=comment_id)
		if comment.commenter.id != request.user.id:
			return HttpResponse(jason.dumps({error:"Access denied."}), content_type='application/json')
		comment.content = content
		comment.date_stamp = datetime.now()
		comment.save()
		return HttpResponse(json.dumps({'comment_id':comment.id}), content_type='application/json')

	scope = request.POST.get('scope', '')
	if not scope:
		scope = 'public'
	else:
		scope = 'private'
	#New comment on a post
	parent_post_id = request.POST.get('parent_post_id','')
	if parent_post_id:
		if not PostModel.objects.filter(id=parent_post_id).exists():
			return HttpResponse(jason.dumps({error:"The parent post dosen't exist."}), content_type='application/json')
		parent_post = PostModel.objects.get(id=parent_post_id)
		if not can_view_post(parent_post, request.user):
			return HttpResponse(jason.dumps({error:"Access denied."}), content_type='application/json')
		
		comment = CommentModel.objects.create(date_stamp=datetime.now(), content=content, scope=scope,\
			parent_post = parent_post, commenter=request.user)
		comment.save()
		return HttpResponse(json.dumps({'comment_id':comment.id,'scope':scope, 'commenter':comment.commenter.username}), content_type='application/json')

	#New comment on another comment
	parent_comment_id = request.POST.get('parent_comment_id','')
	if parent_comment_id:
		if not CommentModel.objects.filter(id=parent_comment_id).exists():
			return HttpResponse(jason.dumps({error:"The parent comment dosen't exist."}), content_type='application/json')
		
		parent_comment = CommentModel.objects.get(id=parent_comment_id)

		if parent_comment.parent_comment:
			comment = CommentModel.objects.create(date_stamp=datetime.now(), content=content, scope=scope,\
			parent_comment = parent_comment.parent_comment, commenter=request.user, reply_to = parent_comment.commenter)
			comment.save()
			return HttpResponse(json.dumps({'comment_id':comment.id,'scope':scope,'commenter':comment.commenter.username,'reply_to':comment.reply_to.username}), content_type='application/json')

		comment = CommentModel.objects.create(date_stamp=datetime.now(), content=content, scope=scope,\
			parent_comment = parent_comment, commenter=request.user)						
		comment.save()
		return HttpResponse(json.dumps({'comment_id':comment.id,'scope':scope,'commenter':comment.commenter.username}), content_type='application/json')

def delete_comment(request, comment_id):
	if not CommentModel.objects.filter(id=comment_id).exists():
		return HttpResponse(jason.dumps({error:"The comment dosen't exist."}), content_type='application/json')
	comment = CommentModel.objects.get(id=comment_id)
	#Only the creator or the superuser can delete a comment. 
	if comment.commenter.id != request.user.id and not user.is_superuser:
		return HttpResponse(jason.dumps({error:"Access denied."}), content_type='application/json')
	comment.delete()
	return HttpResponse(json.dumps({'comment_id':comment.id}), content_type='application/json')


		