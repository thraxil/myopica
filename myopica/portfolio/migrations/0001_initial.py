# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import myopica.portfolio.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('ordinality', models.PositiveSmallIntegerField(default=myopica.portfolio.models.count_galleries)),
            ],
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinality', models.PositiveSmallIntegerField(default=myopica.portfolio.models.count_images)),
                ('gallery', models.ForeignKey(to='portfolio.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(max_length=256, editable=False)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('medium', models.CharField(max_length=256, blank=True)),
                ('ahash', models.CharField(default=b'', max_length=256, null=True)),
                ('extension', models.CharField(default=b'.jpg', max_length=256, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='image',
            field=models.ForeignKey(to='portfolio.Image'),
        ),
    ]
