from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^login/$', views.user_login),
	url(r'^logout/$', views.user_logout),
	url(r'^register/$', views.register),

	#The default redirect url after login
	url(r'^profile/$', views.profile),
]