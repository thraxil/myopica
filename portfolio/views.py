from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
from django.contrib.auth.decorators import login_required
from forms import *
from django.template.defaultfilters import slugify
import urllib2
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
from simplejson import loads
import os


def index(request):
    images = Image.objects.all().order_by("-created")[:15]
    galleries = Gallery.objects.all().order_by("ordinality")
    return render_to_response("index.html",dict(images=images,galleries=galleries))

def stream(request):
    return render_to_response("stream.html",dict(images=Image.objects.all().order_by("-id")[:15]))

def scroll(request,id):
    return render_to_response("scroll.html",dict(images=Image.objects.filter(id__lt=id).order_by("-id")[:15]))

def gallery(request,slug):
    gallery = get_object_or_404(Gallery,slug=slug)
    return render_to_response("gallery.html",dict(gallery=gallery))

def reorder_gallery(request,slug):
    gallery = get_object_or_404(Gallery,slug=slug)
    if request.method == "GET":
        return render_to_response("reorder_gallery.html",dict(gallery=gallery))
    else:
        for k in request.POST.keys():
            if not k.startswith('image-'):
                continue
            ordinality = int(request.POST[k])
            image = get_object_or_404(Image,id=k[len('image-'):])
            gi = get_object_or_404(GalleryImage,gallery=gallery,image=image)
            gi.ordinality = ordinality
            gi.save()
        return HttpResponse("POST")


def gallery_image(request,gallery_slug,image_slug):
    gallery = get_object_or_404(Gallery,slug=gallery_slug)
    image = get_object_or_404(Image,slug=image_slug)
    gi = get_object_or_404(GalleryImage,gallery=gallery,image=image)
    return render_to_response("gallery_image.html",dict(gallery=gallery,
                                                        image=image,
                                                        gi=gi))

def image(request,slug):
    image = get_object_or_404(Image,slug=slug)
    return render_to_response("image.html",dict(image=image))

def image_sets(request,slug,gallery_slug=None):
    image = get_object_or_404(Image,slug=slug)
    galleries = Gallery.objects.all()
    gallery = None
    gi = None
    next_image = None
    if gallery_slug is not None:
        gallery = get_object_or_404(Gallery,slug=gallery_slug)
        gi = get_object_or_404(GalleryImage,gallery=gallery,image=image)
        next_image = gi.next_image()
    if request.method == "POST":
        image_galleries = [gi.gallery for gi in image.galleryimage_set.all()]
        post_galleries = [get_object_or_404(Gallery,id=key[len("gallery_"):]) for key in request.POST.keys() if key.startswith('gallery_')]
        # remove any that need to be removed
        for g in image_galleries:
            if g not in post_galleries:
                image.remove_from_gallery(g)
        # add any missing
        for g in post_galleries:
            image.add_to_gallery(g)

        if request.POST['submit'] == "update":
            return HttpResponseRedirect(request.META.get('HTTP_REFERER',image.get_absolute_url() + "sets/"))
        else:
            # save and next
            if gallery == None:
                # next image by date
                next_image = image.next_image()
            return HttpResponseRedirect(next_image.get_absolute_url() + "sets/")

    else:
        gdata = []
        for g in galleries:
            image_in = g.has_image(image)
            gdata.append(dict(image_in=image_in,gallery=g))

        return render_to_response("image_sets.html",dict(image=image,galleries=gdata))


@login_required
def add_image(request):
    if request.method == "POST":
        if request.POST.get("slug","") == "":
            request.POST['slug'] = slugify(request.POST.get("title"))
        form = AddImageForm(request.POST,request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            if request.FILES.get('image',None):
                original_filename = request.FILES['image'].name
                extension = os.path.splitext(original_filename)[1].lower()
                if extension == ".jpeg":
                    extension = ".jpg"
                if extension not in [".jpg",".png",".gif"]:
                    return HttpResponse("unsupported image format")
                register_openers()
                datagen, headers = multipart_encode((
                        ("t","upload"),
                        MultipartParam(name='image',fileobj=request.FILES['image'],
                                       filename="image%s" % extension)))
                req = urllib2.Request("http://apomixis.thraxil.org/", datagen, headers)
                metadata = loads(urllib2.urlopen(req).read())
                img.ahash = metadata["hash"]
                img.extension = extension

            img.save()
            for key in request.POST.keys():
                if key.startswith("gallery_"):
                    g = get_object_or_404(Gallery,id=key[len("gallery_"):])
                    img.add_to_gallery(g)

            return HttpResponseRedirect(img.get_absolute_url())
        else:
            print "not valid"
            galleries = Gallery.objects.all()
            return render_to_response("add_image.html",dict(galleries=galleries,
                                                            form=form))
    else:
        galleries = Gallery.objects.all()
        return render_to_response("add_image.html",dict(galleries=galleries,
                                                    form=AddImageForm()))


