from ..models import Image, Gallery

from django.test import TestCase


class ImageTest(TestCase):
    def test_str(self):
        i = Image.objects.create(
            title="test",
            slug="test",
        )
        self.assertEqual(str(i), i.title)


class GalleryTest(TestCase):
    def test_str(self):
        g = Gallery.objects.create(
            title="test",
            slug="test",
        )
        self.assertEqual(str(g), g.title)
