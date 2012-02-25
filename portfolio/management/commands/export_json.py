from django.core.management.base import BaseCommand
import portfolio.models
from django.conf import settings
from simplejson import loads

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        d = dict()
        galleries = []
        for g in portfolio.models.Gallery.objects.all():
            g_data = dict(id=g.id,
                          title=g.title,
                          slug=g.slug,
                          description=g.description,
                          ordinality=g.ordinality)
            galleries.append(g_data)
        d['galleries'] = galleries
        images = []
        for i in portfolio.models.Image.objects.all():
            i_data = dict(id=i.id,
                          title = i.title,
                          slug = i.slug,
                          description = i.description,
                          created = str(i.created),
                          medium = i.medium,
                          ahash = i.ahash,
                          extension = i.extension)
            images.append(i_data)
        d['images'] = images
        galleryimages = []
        for gi in portfolio.models.GalleryImage.objects.all():
            gi_data = dict(gallery_id=gi.gallery.id,
                           image_id=gi.image.id,
                           ordinality=gi.ordinality)
            galleryimages.append(gi_data)
        d['galleryimages'] = galleryimages
        print dumps(d)






