from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from myopica.portfolio.feeds import MainFeed

urlpatterns = patterns('',
                       (r'^$', 'myopica.portfolio.views.index'),
                       (r'^stream/$','myopica.portfolio.views.stream'),
                       (r'^scroll/(?P<id>\d+)/$','myopica.portfolio.views.scroll'),
                       (r'^feeds/(?P<url>.*)/$', MainFeed()),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/myopica/media/'}),
                       (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/tmp/myopica/media/'}),
                       (r'^image/(?P<slug>[^/]+)/$', 'myopica.portfolio.views.image'),
                       (r'^image/(?P<slug>[^/]+)/sets/$', 'myopica.portfolio.views.image_sets'),                       
                       (r'^add_image/$', 'myopica.portfolio.views.add_image'),
                       (r'^(?P<slug>[^/]+)/$', 'myopica.portfolio.views.gallery'),
                       (r'^(?P<slug>[^/]+)/reorder/$', 'myopica.portfolio.views.reorder_gallery'),                       
                       (r'^(?P<gallery_slug>[^/]+)/(?P<image_slug>[^/]+)/$', 'myopica.portfolio.views.gallery_image'),
                       (r'^(?P<gallery_slug>[^/]+)/(?P<slug>[^/]+)/sets/$', 'myopica.portfolio.views.image_sets'),                       

)
