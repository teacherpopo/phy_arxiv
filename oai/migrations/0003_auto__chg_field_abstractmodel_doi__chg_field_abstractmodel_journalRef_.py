# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AbstractModel.doi'
        db.alter_column(u'oai_abstractmodel', 'doi', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'AbstractModel.journalRef'
        db.alter_column(u'oai_abstractmodel', 'journalRef', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'AbstractModel.licenseStr'
        db.alter_column(u'oai_abstractmodel', 'licenseStr', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

    def backwards(self, orm):

        # Changing field 'AbstractModel.doi'
        db.alter_column(u'oai_abstractmodel', 'doi', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AbstractModel.journalRef'
        db.alter_column(u'oai_abstractmodel', 'journalRef', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AbstractModel.licenseStr'
        db.alter_column(u'oai_abstractmodel', 'licenseStr', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'datestamp': ('django.db.models.fields.DateField', [], {}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateField', [], {'null': 'True'})
        }
    }

    complete_apps = ['oai']