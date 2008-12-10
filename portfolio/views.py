from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
import flickrapi
from django.contrib.auth.decorators import login_required
from forms import *
from django.template.defaultfilters import slugify
from datetime import datetime

def index(request):
    images = Image.objects.all().order_by("-created")[:15]
    galleries = Gallery.objects.all().order_by("ordinality")
    return render_to_response("index.html",dict(images=images,galleries=galleries))

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
            img = form.save()
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

import os
class FlickrImage:
    def __init__(self,flickr,id):
        self.flickr = flickr
        self.id = id
        self.title = ""
        self.taken = ""
        self.uri = ""
        self.date = "" #datetime.datetime.fromtimestamp(1130288532)
        self.galleries = []

    def add_gallery(self,gallery):
        self.galleries.append(gallery)

    def download(self):
        base = "/var/tmp/myopica/media/"
        d = datetime.fromtimestamp(int(self.date))
        subdir = "images/%04d/%02d/%02d/" % (d.year,d.month,d.day)
        dir = base + subdir
        try:
            os.makedirs(dir)
        except:
            pass
        os.system("wget %s -P %s" % (self.url,dir))
        filename = subdir + self.url.split("/")[-1]
        return filename

    def create(self):
        slug = slugify(self.title)
        created = datetime.fromtimestamp(int(self.date))
        image = self.download()
        i = Image.objects.create(slug=slug,title=self.title,image=image,created=created,description="",medium="")
        for g in self.galleries:
            i.add_to_gallery(g)

import sys
def import_from_flickr(request):
    flickr = flickrapi.FlickrAPI("a3a8f82088e88d4228bbd169eea1d721")
    sets = """sketches|large moleskine|small moleskine|one hour paintings|nearsighted and obsessive compulsive|myopica|volume 3|error and annihilation|abstract comics"""
    flickr_sets = """621508|1520905|1550023|72157600068913439|72157594319315437|72157602372213076|72157603370455679|72157602921751456|72157602683198578"""
    tags = "oil|pencil|abstract|watercolor|penink|colored pencil|acrylic"
    flickr_tags = "oil|pencil|abstract|watercolor|pen|coloredpencil|acrylic"

    sets_map = dict()
    tags_map = dict()

    images = dict()
    def get_or_create_fi(id):
        if id in images.keys():
            return images[id]
        else:
            fi = FlickrImage(flickr,id)
            images[id] = fi
            return fi

    for (set,id) in zip(sets.split("|"),flickr_sets.split("|")):
        slug = slugify(set)
        gallery = get_object_or_404(Gallery,slug=slug)
        sets_map[slug] = (gallery,id)
        photos = flickr.photosets_getPhotos(photoset_id=id,extras="date_upload,date_taken")

        for photo in photos.photoset[0].photo:
            i = get_or_create_fi(photo['id'])
            i.title = photo['title']
            i.date = photo['dateupload']
            i.add_gallery(gallery)
    for (tag,flickrtag) in zip(tags.split("|"),flickr_tags.split("|")):
        slug = slugify(tag)
        gallery = get_object_or_404(Gallery,slug=slug)
        tags_map[slug] = (gallery,flickrtag)

    for fi in sorted(images.values(),key=lambda x: x.date):
        d = datetime.fromtimestamp(int(fi.date))
        if d < datetime(2007,02,28):
            continue
        print fi.title
        print fi.date
        info = flickr.photos_getInfo(photo_id=fi.id,format='etree')

        print str(info.find('photo').find('tags').findall('tag'))
        for tag in info.find('photo').find('tags').findall('tag'):
            if tags_map.has_key(tag.attrib['raw']):
                gallery = tags_map[tag.attrib['raw']][0]
                fi.add_gallery(gallery)
        print str(fi.galleries)
        photo = info.find('photo')
        farm = photo.attrib['farm']
        server = photo.attrib['server']
        secret = photo.attrib['secret']
        try:
            secret = photo.attrib['originalsecret']
        except:
            pass
        fi.url = "http://farm%s.static.flickr.com/%s/%s_%s_o.jpg" % (farm, server, fi.id, secret)
        print fi.url
        fi.create()
    return HttpResponse("ok")
        


    
    

