# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AbstractModel.mscClass'
        db.add_column(u'oai_abstractmodel', 'mscClass',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True),
                      keep_default=False)

        # Adding field 'AbstractModel.rating'
        db.add_column(u'oai_abstractmodel', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'AbstractModel.rated'
        db.add_column(u'oai_abstractmodel', 'rated',
                      self.gf('django.db.models.fields.DateField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'AbstractModel.archive'
        db.add_column(u'oai_abstractmodel', 'archive',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    def backwards(self, orm):
        # Deleting field 'AbstractModel.mscClass'
        db.delete_column(u'oai_abstractmodel', 'mscClass')

        # Deleting field 'AbstractModel.rating'
        db.delete_column(u'oai_abstractmodel', 'rating')

        # Deleting field 'AbstractModel.rated'
        db.delete_column(u'oai_abstractmodel', 'rated')

        # Deleting field 'AbstractModel.archive'
        db.delete_column(u'oai_abstractmodel', 'archive')


        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=12, null=True))

    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']