from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify


class Image(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, editable=False)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    medium = models.CharField(max_length=256, blank=True)
    ahash = models.CharField(max_length=256, default="", null=True)
    extension = models.CharField(max_length=256, default=".jpg", null=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.title)[:255]
        addto = 1
        while Image.objects.filter(slug=slug).count() > 0:
            slug = slug + str(addto)
            addto += 1
        self.slug = slug
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/image/%s/" % self.slug

    def add_to_gallery(self, gallery):
        if GalleryImage.objects.filter(
                image=self,
                gallery=gallery).count() > 0:
            return
        GalleryImage.objects.create(
            image=self, gallery=gallery,
            ordinality=gallery.galleryimage_set.all().count() + 1)
        gallery.update_ordinality()

    def remove_from_gallery(self, gallery):
        gi = GalleryImage.objects.filter(gallery=gallery, image=self)[0]
        gi.delete()
        gallery.update_ordinality()

    def prev_image(self):
        r = Image.objects.filter(created__gt=self.created).order_by("created")
        if r.count():
            return r[0]
        else:
            return None

    def next_image(self):
        r = Image.objects.filter(created__lt=self.created).order_by("-created")
        if r.count():
            return r[0]
        else:
            return None


class ImageAdmin(admin.ModelAdmin):
    pass


def count_galleries():
    return Gallery.objects.all().count()


class Gallery(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    ordinality = models.PositiveSmallIntegerField(default=count_galleries)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/" % self.slug

    def images(self):
        return [i.image
                for i
                in self.galleryimage_set.all().order_by("-ordinality")]

    def all_images(self):
        return [i.image
                for i
                in self.galleryimage_set.all().order_by("ordinality")]

    def first_images(self):
        return [i.image
                for i
                in self.galleryimage_set.all().order_by("-ordinality")][:15]

    def first_image(self):
        return self.galleryimage_set.all().order_by(
            "-ordinality").first().image

    def newest_images(self):
        return [i.image
                for i in self.galleryimage_set.all().order_by("-id")][:5]

    def update_ordinality(self):
        cnt = 1
        for gi in self.galleryimage_set.all().order_by("ordinality"):
            gi.ordinality = cnt
            gi.save()
            cnt += 1

    def has_image(self, image):
        gallery_ids = [gi.gallery.id for gi in image.galleryimage_set.all()]
        return self.id in gallery_ids


def count_images():
    return Image.objects.all().count()


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'ordinality')


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    ordinality = models.PositiveSmallIntegerField(default=count_images)

    def __unicode__(self):
        return u"%s [%02d] %s" % (self.gallery, self.ordinality,
                                  self.image)

    def prev_image(self):
        r = GalleryImage.objects.filter(
            gallery=self.gallery,
            ordinality__gte=self.ordinality
        ).exclude(
            image=self.image
        ).order_by("ordinality", "image")
        if r.count():
            return r[0]
        else:
            return None

    def next_image(self):
        r = GalleryImage.objects.filter(
            gallery=self.gallery,
            ordinality__lte=self.ordinality
        ).exclude(
            image=self.image
        ).order_by("-ordinality", "-image")
        if r.count():
            return r[0]
        else:
            return None

    def get_absolute_url(self):
        return self.gallery.get_absolute_url() + self.image.slug + "/"

    def has_other_galleries(self):
        return self.other_galleries().count() > 0

    def other_galleries(self):
        return self.image.galleryimage_set.all().exclude(gallery=self.gallery)


class GalleryImageAdmin(admin.ModelAdmin):
    pass
