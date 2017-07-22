import django.contrib.sitemaps.views
import django.contrib.auth.views
import django.views.static

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.views.generic.detail import DetailView
from myopica.portfolio import views

from myopica.portfolio.feeds import MainFeed
from myopica.portfolio.models import Gallery, Image

admin.autodiscover()

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

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^feeds/(?P<url>.*)/$', MainFeed()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', django.contrib.sitemaps.views.sitemap,
        {'sitemaps': sitemaps}),
    url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': '/var/tmp/myopica/media/'}),
    url(r'^image/(?P<slug>[^/]+)/$', DetailView.as_view(model=Image)),
    url(r'^image/(?P<slug>[^/]+)/sets/$', views.ImageSetsView.as_view()),
    url(r'^add_image/$', views.AddImageView.as_view()),
    url(r'^(?P<slug>[^/]+)/$', DetailView.as_view(model=Gallery)),
    url(r'^(?P<slug>[^/]+)/reorder/$',
        views.ReorderGalleryView.as_view()),
    url(r'^(?P<gallery_slug>[^/]+)/(?P<image_slug>[^/]+)/$',
        views.GalleryImageView.as_view()),
    url(r'^(?P<gallery_slug>[^/]+)/(?P<slug>[^/]+)/sets/$',
        views.ImageSetsView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
