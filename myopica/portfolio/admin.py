from django.contrib import admin
from models import (
    Image, ImageAdmin,
    Gallery, GalleryAdmin,
    GalleryImage, GalleryImageAdmin)


admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
