from django.conf.urls import url
from . import views


urlpatterns = [

	#Edit the post with id == post_id
	url(r'^(?P<post_id>\d+)/$', views.post_editor, name='edit_post'),

	#Start a new document
	url(r'^new/$', views.new_editor, name='new_post'),

	#Save a draft (implemented with ajax)
	url(r'^save/$', views.save_draft, name='save_post'),

	#Submit a draft and turn its status to "post"
	url(r'^submit/$', views.submit, name='submit_post'),

	#Deleta a draft
	url(r'delete/(?P<post_id>\d+)/$', views.delete, name='delete_post'),
]