# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AbstractModel.categories'
        db.add_column(u'oai_abstractmodel', 'categories',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)

        # Adding field 'AbstractModel.authors'
        db.add_column(u'oai_abstractmodel', 'authors',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AbstractModel.categories'
        db.delete_column(u'oai_abstractmodel', 'categories')

        # Deleting field 'AbstractModel.authors'
        db.delete_column(u'oai_abstractmodel', 'authors')


    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'authors': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.TextField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'datestamp': ('django.db.models.fields.DateField', [], {}),
            'doi': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']