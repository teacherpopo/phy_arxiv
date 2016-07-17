from django.conf.urls import url
from . import views


urlpatterns = [

	#View the post with id == post_id
	url(r'^(?P<post_id>\d+)/$', views.view_post, name='view_post'),

	url(r'^comment/save/$', views.save_comment, name='save_comment'),
	url(r'^comment/delete/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
]