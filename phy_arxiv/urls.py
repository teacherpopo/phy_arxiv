from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from accounts import urls as accounts_urls
from editor import urls as editor_urls
from post import urls as post_urls
from oai import urls as oai_urls
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phy_arxiv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #Set the profile page as the default portal
    url(r'^$', RedirectView.as_view(url='/accounts/profile/')),

    #Account management
    url(r'^accounts/', include(accounts_urls)),

    #Edit posts
    url(r'^editor/', include(editor_urls)),

    #View posts
    url(r'^post/', include(post_urls)),

		#View arXiv/OAI
		url(r'^oai/', include(oai_urls)),
)
