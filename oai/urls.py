from django.conf.urls import url
from . import views


urlpatterns = [

	url(r'^$', views.oai, name='oai'),
	url(r'^filter/$', views.oai_filter, name='oai_filter'),
	url(r'^cache/$', views.oai_cache, name='oai_cache'),
	url(r'^size/$', views.oai_size, name='oai_size'),
	url(r'^rate/$', views.oai_rate, name='oai_rate'),
	url(r'^archive/$', views.oai_archive, name='oai_archive'),
]
