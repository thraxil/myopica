from ..models import Image, Gallery
from ..views import GalleryImageView
from django.test import RequestFactory, TestCase
from django.test.client import Client


class TestGalleryImageView(TestCase):
    def setUp(self):
        self.c = Client()

    def test_view(self):
        i = Image.objects.create(title="test", slug="test")
        g = Gallery.objects.create(title="test", slug="test")
        i.add_to_gallery(g)

        v = GalleryImageView.as_view()
        req = RequestFactory().get('/{}/{}/'.format(g.slug, i.slug))
        r = v(req, gallery_slug=g.slug, image_slug=i.slug).render()
        self.assertEqual(r.status_code, 200)
