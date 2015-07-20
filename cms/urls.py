# -*- coding: utf-8 -*-
from cms.apphook_pool import apphook_pool
from cms.views import details
from django.conf import settings
from django.conf.urls.defaults import url, patterns
from WLSite import resource_views

if settings.APPEND_SLASH:
    reg = url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/$', details, name='pages-details-by-slug')
else:
    reg = url(r'^(?P<slug>[0-9A-Za-z-_.//]+)$', details, name='pages-details-by-slug')

urlpatterns = [
    url(r'^$', 'resource_views.resourceView'),
    url(r'^(?P<published_id>[0-9]+)/(?P<draft_id>[0-9]+)/privacy/(?P<setting>[0-9]+)/$', 'resource_views.setPagePrivacy'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/title/(?P<new_title>.+)/$', 'resource_views.changeTitle'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/add_to_gallery/$', 'resource_views.addResourceToGallery'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/rate/$', 'resource_views.changeRating'),
    url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/edit-tags/$', 'resource_views.changeTags'),
    # Public pages
    url(r'^$', details, {'slug':''}, name='pages-root'),
    reg,
]

if apphook_pool.get_apphooks():
    """If there are some application urls, add special resolver, so we will
    have standard reverse support.
    """
    from cms.appresolver import get_app_patterns
    urlpatterns = get_app_patterns() + urlpatterns
    
urlpatterns = patterns('', *urlpatterns)