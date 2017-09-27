from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import Image


class MainFeed(Feed):
    title = "Myopica Newest Images"
    link = "/"
    description = ""
    feed_type = Atom1Feed

    def items(self):
        return Image.objects.order_by('-created')[:5]
