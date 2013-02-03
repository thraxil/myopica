# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('portfolio_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('ahash', self.gf('django.db.models.fields.CharField')(default='', max_length=256, null=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(default='.jpg', max_length=256, null=True)),
        ))
        db.send_create_signal('portfolio', ['Image'])

        # Adding model 'Gallery'
        db.create_table('portfolio_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ordinality', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('portfolio', ['Gallery'])

        # Adding model 'GalleryImage'
        db.create_table('portfolio_galleryimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Gallery'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Image'])),
            ('ordinality', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('portfolio', ['GalleryImage'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('portfolio_image')

        # Deleting model 'Gallery'
        db.delete_table('portfolio_gallery')

        # Deleting model 'GalleryImage'
        db.delete_table('portfolio_galleryimage')


    models = {
        'portfolio.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordinality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'portfolio.galleryimage': {
            'Meta': {'object_name': 'GalleryImage'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portfolio.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portfolio.Image']"}),
            'ordinality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'portfolio.image': {
            'Meta': {'object_name': 'Image'},
            'ahash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'default': "'.jpg'", 'max_length': '256', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['portfolio']
