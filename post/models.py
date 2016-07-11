from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PostModel(models.Model):
	# The "id" field is by default an auto-incrementing field.
	# Could change it to a random key.

	#Date and time of the last modification
	date_stamp = models.DateTimeField()

	title = models.CharField(max_length=100)
	content = models.TextField()

	#A "draft" turns into a "post" after submission 
	status = models.CharField(max_length=20)

	#"private" or "public", default is "private".
	scope = models.CharField(max_length=20)
	
	owner = models.ForeignKey(User, related_name='owner')
	authors = models.ManyToManyField(User, related_name='authors')

	def __unicode__(self):
		return self.title

class CommentModel(models.Model):
	date_stamp = models.DateTimeField()
	content = models.TextField()

	#"private" or "public", default is "private".
	scope = models.CharField(max_length=20)

	#The parent post a comment belongs to.
	parent_post = models.ForeignKey(PostModel, related_name='comments')

	commenter = models.ForeignKey(User, related_name='commenter')
	#A commenter can specify a user to reply to.
	reply_to = models.ForeignKey(User, null=True, blank=True, related_name = 'reply_to')