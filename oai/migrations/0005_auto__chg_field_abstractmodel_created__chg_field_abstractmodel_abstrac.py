# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AbstractModel.created'
        db.alter_column(u'oai_abstractmodel', 'created', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'AbstractModel.abstract'
        db.alter_column(u'oai_abstractmodel', 'abstract', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'AbstractModel.title'
        db.alter_column(u'oai_abstractmodel', 'title', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'AbstractModel.authors'
        db.alter_column(u'oai_abstractmodel', 'authors', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'AbstractModel.datestamp'
        db.alter_column(u'oai_abstractmodel', 'datestamp', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=12, null=True))

        # Changing field 'AbstractModel.categories'
        db.alter_column(u'oai_abstractmodel', 'categories', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'AbstractModel.created'
        db.alter_column(u'oai_abstractmodel', 'created', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'AbstractModel.abstract'
        db.alter_column(u'oai_abstractmodel', 'abstract', self.gf('django.db.models.fields.TextField')(default=None))

        # Changing field 'AbstractModel.title'
        db.alter_column(u'oai_abstractmodel', 'title', self.gf('django.db.models.fields.CharField')(default=None, max_length=300))

        # Changing field 'AbstractModel.authors'
        db.alter_column(u'oai_abstractmodel', 'authors', self.gf('django.db.models.fields.TextField')(default=None))

        # Changing field 'AbstractModel.datestamp'
        db.alter_column(u'oai_abstractmodel', 'datestamp', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=12))

        # Changing field 'AbstractModel.categories'
        db.alter_column(u'oai_abstractmodel', 'categories', self.gf('django.db.models.fields.TextField')(default=None))

    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'categories': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'datestamp': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']