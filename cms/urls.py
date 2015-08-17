# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, patterns
from cms.apphook_pool import apphook_pool
from cms.appresolver import get_app_patterns
from cms.views import details

# This is a constant, really, but must live here due to import order
SLUG_REGEXP = '[0-9A-Za-z-_.//]+'

if settings.APPEND_SLASH:
    regexp = r'^(?P<slug>%s)/$' % SLUG_REGEXP
else:
    regexp = r'^(?P<slug>%s)$' % SLUG_REGEXP

if apphook_pool.get_apphooks():
    # If there are some application urls, use special resolver,
    # so we will have standard reverse support.
    urlpatterns = get_app_patterns()
else:
    urlpatterns = [
        url(r'^$', 'WLSite.resource_views.resourceView'),
        url(r'^(?P<published_id>[0-9]+)/(?P<draft_id>[0-9]+)/privacy/(?P<setting>[0-9]+)/$', 'WLSite.resource_views.setPagePrivacy'),
        url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/title/(?P<new_title>.+)/$', 'WLSite.resource_views.changeTitle'),
        url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/add_to_gallery/$', 'WLSite.resource_views.addResourceToGallery'),
        url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/rate/$', 'WLSite.resource_views.changeRating'),
        url(r'^(?P<slug>[0-9A-Za-z-_.//]+)/edit-tags/$', 'WLSite.resource_views.changeTags'),
    ]

# Public pages
urlpatterns.extend([
    url(regexp, details, name='pages-details-by-slug'),
    url(r'^$', details, {'slug': ''}, name='pages-root'),
])