from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap

admin.autodiscover()

from myopica.portfolio.feeds import MainFeed
from myopica.portfolio.models import Gallery, Image

gallery_info_dict = {
    'queryset': Gallery.objects.all(),
}

image_info_dict = {
    'queryset': Image.objects.all(),
    'date_field': 'created',
}

sitemaps = {
    'galleries': GenericSitemap(gallery_info_dict, priority=0.6),
    'images': GenericSitemap(image_info_dict, priority=0.6),
}

urlpatterns = patterns(
    '',
    (r'^$', 'myopica.portfolio.views.index'),
    (r'^stream/$', 'myopica.portfolio.views.stream'),
    (r'^scroll/(?P<id>\d+)/$', 'myopica.portfolio.views.scroll'),
    (r'^feeds/(?P<url>.*)/$', MainFeed()),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': '/home/anders/code/python/myopica/media/'}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': '/var/tmp/myopica/media/'}),
    (r'^image/(?P<slug>[^/]+)/$', 'myopica.portfolio.views.image'),
    (r'^image/(?P<slug>[^/]+)/sets/$',
     'myopica.portfolio.views.image_sets'),
    (r'^add_image/$', 'myopica.portfolio.views.add_image'),
    (r'^(?P<slug>[^/]+)/$', 'myopica.portfolio.views.gallery'),
    (r'^(?P<slug>[^/]+)/reorder/$',
     'myopica.portfolio.views.reorder_gallery'),
    (r'^(?P<gallery_slug>[^/]+)/(?P<image_slug>[^/]+)/$',
     'myopica.portfolio.views.gallery_image'),
    (r'^(?P<gallery_slug>[^/]+)/(?P<slug>[^/]+)/sets/$',
     'myopica.portfolio.views.image_sets'),
)
