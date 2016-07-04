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
	
	owner = models.ForeignKey(User, related_name='owner')
	authors = models.ManyToManyField(User, related_name='authors')

	def __unicode__(self):
		return self.title