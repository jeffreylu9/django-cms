# -*- coding: utf-8 -*-
from django.conf import settings

from cms.apphook_pool import apphook_pool
from cms.appresolver import get_app_patterns
from cms.views import details

from django.conf.urls import url, patterns
from WLSite import resource_views

# This is a constant, really, but must live here due to import order
SLUG_REGEXP = '[0-9A-Za-z-_.//]+'

reg = None
if settings.APPEND_SLASH:
    regexp = r'^(?P<slug>%s)/$' % SLUG_REGEXP
else:
    regexp = r'^(?P<slug>%s)$' % SLUG_REGEXP
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
    # If there are some application urls, use special resolver,
    # so we will have standard reverse support.
    urlpatterns = get_app_patterns()
else:
    urlpatterns = []

urlpatterns.extend([
    url(regexp, details, name='pages-details-by-slug'),
    url(r'^$', details, {'slug': ''}, name='pages-root'),
])
