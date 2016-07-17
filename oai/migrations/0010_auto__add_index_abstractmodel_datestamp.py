# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'AbstractModel', fields ['datestamp']
        db.create_index(u'oai_abstractmodel', ['datestamp'])


    def backwards(self, orm):
        # Removing index on 'AbstractModel', fields ['datestamp']
        db.delete_index(u'oai_abstractmodel', ['datestamp'])


    models = {
        u'oai.abstractmodel': {
            'ACMClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'MSCClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'Meta': {'ordering': "['-datestamp']", 'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'categories': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'datestamp': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'null': 'True'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'rated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'reportNo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']