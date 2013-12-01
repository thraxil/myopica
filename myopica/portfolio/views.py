from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from models import Gallery, Image, GalleryImage
from django.contrib.auth.decorators import login_required
from forms import AddImageForm
from django.template.defaultfilters import slugify
from simplejson import loads
import os
import requests


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        images = Image.objects.all().order_by("-created")[:15]
        galleries = Gallery.objects.all().order_by("ordinality")
        return dict(images=images, galleries=galleries)


class StreamView(TemplateView):
    template_name = "stream.html"

    def get_context_data(self):
        return dict(images=Image.objects.all().order_by("-id")[:15])


class ScrollView(TemplateView):
    template_name = "scroll.html"

    def get_context_data(self, id):
        return(
            dict(images=Image.objects.filter(id__lt=id).order_by("-id")[:15]))


class GalleryView(DetailView):
    model = Gallery
    template_name = "gallery.html"
    context_object_name = "gallery"


class ReorderGalleryView(View):
    template_name = "reorder_gallery.html"

    def get(self, request, slug):
        gallery = get_object_or_404(Gallery, slug=slug)
        return render(request, self.template_name,
                      dict(gallery=gallery))

    def post(self, request, slug):
        gallery = get_object_or_404(Gallery, slug=slug)
        for k in request.POST.keys():
            if not k.startswith('image-'):
                continue
            ordinality = int(request.POST[k])
            image = get_object_or_404(Image, id=k[len('image-'):])
            gi = get_object_or_404(GalleryImage, gallery=gallery, image=image)
            gi.ordinality = ordinality
            gi.save()
        return HttpResponse("POST")


class GalleryImageView(TemplateView):
    template_name = "gallery_image.html"

    def get_context_data(self, gallery_slug, image_slug):
        gallery = get_object_or_404(Gallery, slug=gallery_slug)
        image = get_object_or_404(Image, slug=image_slug)
        gi = get_object_or_404(GalleryImage, gallery=gallery, image=image)
        return dict(gallery=gallery,
                    image=image,
                    gi=gi)


def image(request, slug):
    image = get_object_or_404(Image, slug=slug)
    return render(request, "image.html", dict(image=image))


def image_sets(request, slug, gallery_slug=None):
    image = get_object_or_404(Image, slug=slug)
    galleries = Gallery.objects.all()
    gallery = None
    gi = None
    next_image = None
    if gallery_slug is not None:
        gallery = get_object_or_404(Gallery, slug=gallery_slug)
        gi = get_object_or_404(GalleryImage, gallery=gallery, image=image)
        next_image = gi.next_image()
    if request.method == "POST":
        image_galleries = [gi.gallery for gi in image.galleryimage_set.all()]
        post_galleries = [get_object_or_404(Gallery, id=key[len("gallery_"):])
                          for key in request.POST.keys()
                          if key.startswith('gallery_')]
        # remove any that need to be removed
        for g in image_galleries:
            if g not in post_galleries:
                image.remove_from_gallery(g)
        # add any missing
        for g in post_galleries:
            image.add_to_gallery(g)

        if request.POST['submit'] == "update":
            return HttpResponseRedirect(
                request.META.get('HTTP_REFERER',
                                 image.get_absolute_url() + "sets/"))
        else:
            # save and next
            if gallery is None:
                # next image by date
                next_image = image.next_image()
            return HttpResponseRedirect(
                next_image.get_absolute_url() + "sets/")

    else:
        gdata = []
        for g in galleries:
            image_in = g.has_image(image)
            gdata.append(dict(image_in=image_in, gallery=g))

        return render(request, "image_sets.html",
                      dict(image=image, galleries=gdata))


@login_required
def add_image(request):
    if request.method == "POST":
        if request.POST.get("slug", "") == "":
            request.POST['slug'] = slugify(request.POST.get("title"))
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            if request.FILES.get('image', None):
                original_filename = request.FILES['image'].name
                extension = os.path.splitext(original_filename)[1].lower()
                if extension == ".jpeg":
                    extension = ".jpg"
                if extension not in [".jpg", ".png", ".gif"]:
                    return HttpResponse("unsupported image format")

                files = {'image':
                         ("image%s" % extension,
                          request.FILES['image'])
                         }
                r = requests.post("http://reticulum.thraxil.org/", files=files)
                img.ahash = loads(r.text)["hash"]
                img.extension = extension

            img.save()
            for key in request.POST.keys():
                if key.startswith("gallery_"):
                    g = get_object_or_404(Gallery, id=key[len("gallery_"):])
                    img.add_to_gallery(g)

            return HttpResponseRedirect(img.get_absolute_url())
        else:
            print "not valid"
            galleries = Gallery.objects.all()
            return render(request, "add_image.html",
                          dict(galleries=galleries,
                               form=form))
    else:
        galleries = Gallery.objects.all()
        return render(request, "add_image.html",
                      dict(galleries=galleries,
                           form=AddImageForm()))
