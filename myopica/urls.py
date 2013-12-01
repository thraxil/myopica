from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.views.generic.detail import DetailView
from myopica.portfolio import views

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
    (r'^$', views.IndexView.as_view()),
    (r'^feeds/(?P<url>.*)/$', MainFeed()),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': '/var/tmp/myopica/media/'}),
    (r'^image/(?P<slug>[^/]+)/$', DetailView.as_view(model=Image)),
    (r'^image/(?P<slug>[^/]+)/sets/$', views.ImageSetsView.as_view()),
    (r'^add_image/$', views.AddImageView.as_view()),
    (r'^(?P<slug>[^/]+)/$', DetailView.as_view(model=Gallery)),
    (r'^(?P<slug>[^/]+)/reorder/$',
     views.ReorderGalleryView.as_view()),
    (r'^(?P<gallery_slug>[^/]+)/(?P<image_slug>[^/]+)/$',
     views.GalleryImageView.as_view()),
    (r'^(?P<gallery_slug>[^/]+)/(?P<slug>[^/]+)/sets/$',
     views.ImageSetsView.as_view()),
)
