from django.conf.urls import url
from . import views


urlpatterns = [

	#View the post with id == post_id
	url(r'^(?P<post_id>\d+)/$', views.view_post, name='view_post'),
]