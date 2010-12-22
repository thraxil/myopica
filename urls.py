from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from portfolio.feeds import MainFeed, GalleryFeed

feeds = {
    'main': MainFeed,
    'gallery' : GalleryFeed,
    }

urlpatterns = patterns('',
                       (r'^$', 'myopica.portfolio.views.index'),
                       (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/myopica/media/'}),
                       (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/tmp/myopica/media/'}),
                       (r'^image/(?P<slug>[^/]+)/$', 'myopica.portfolio.views.image'),
                       (r'^image/(?P<slug>[^/]+)/sets/$', 'myopica.portfolio.views.image_sets'),                       
                       (r'^import_from_flickr/$','myopica.portfolio.views.import_from_flickr'),
                       (r'^add_image/$', 'myopica.portfolio.views.add_image'),
                       (r'^(?P<slug>[^/]+)/$', 'myopica.portfolio.views.gallery'),
                       (r'^(?P<slug>[^/]+)/reorder/$', 'myopica.portfolio.views.reorder_gallery'),                       
                       (r'^(?P<gallery_slug>[^/]+)/(?P<image_slug>[^/]+)/$', 'myopica.portfolio.views.gallery_image'),
                       (r'^(?P<gallery_slug>[^/]+)/(?P<slug>[^/]+)/sets/$', 'myopica.portfolio.views.image_sets'),                       

)
