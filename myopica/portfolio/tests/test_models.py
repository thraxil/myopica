from ..models import Image

from django.test import TestCase


class ImageTest(TestCase):
    def test_str(self):
        i = Image.objects.create(
            title="test",
            slug="test",
        )
        self.assertEqual(str(i), i.title)
