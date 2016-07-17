# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AbstractModel.abstract'
        db.alter_column(u'oai_abstractmodel', 'abstract', self.gf('django.db.models.fields.TextField')())

        # Changing field 'AbstractModel.title'
        db.alter_column(u'oai_abstractmodel', 'title', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'AbstractModel.authors'
        db.alter_column(u'oai_abstractmodel', 'authors', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'AbstractModel.abstract'
        db.alter_column(u'oai_abstractmodel', 'abstract', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'AbstractModel.title'
        db.alter_column(u'oai_abstractmodel', 'title', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'AbstractModel.authors'
        db.alter_column(u'oai_abstractmodel', 'authors', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "'[abtract]'"}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.TextField', [], {'default': "'[authors]'"}),
            'categories': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'datestamp': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'null': 'True'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'mscClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'rated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'[title]'", 'max_length': '300'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']