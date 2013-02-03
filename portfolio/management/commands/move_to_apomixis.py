from django.core.management.base import BaseCommand
import portfolio.models
import urllib2
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
from simplejson import loads


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        register_openers()
        for i in portfolio.models.Image.objects.all():
            print i.image.path
            imgobj = open(i.image.path)
            datagen, headers = multipart_encode(
                (
                    ("t", "upload"),
                    MultipartParam(
                        name='image', fileobj=imgobj,
                        filename=i.image.path)))
            request = urllib2.Request("http://apomixis.thraxil.org/",
                                      datagen, headers)
            metadata = loads(urllib2.urlopen(request).read())
            print " uploaded to apomixis %s" % metadata["hash"]
            i.ahash = metadata["hash"]
            i.extension = metadata["extension"]
            i.save()
