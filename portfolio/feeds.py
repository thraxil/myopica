from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import FeedDoesNotExist
from models import Gallery,Image,GalleryImage


class MainFeed(Feed):
    title = "Myopica Newest Images"
    link = "/"
    description = ""
    feed_type = Atom1Feed
    
    def items(self):
        return Image.objects.order_by('-created')[:5]

class GalleryFeed(Feed):
    feed_type = Atom1Feed
    
    def get_object(self, bits):
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Gallery.objects.get(slug__exact=bits[0])

    def title(self, obj):
        return "Myopica: %s" % obj.title

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Images in gallery %s" % obj.title

    def items(self, obj):
        return obj.newest_images()




