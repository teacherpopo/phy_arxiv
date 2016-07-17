# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AbstractModel.mscClass'
        db.delete_column(u'oai_abstractmodel', 'mscClass')

        # Adding field 'AbstractModel.MSCClass'
        db.add_column(u'oai_abstractmodel', 'MSCClass',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True),
                      keep_default=False)

        # Adding field 'AbstractModel.ACMClass'
        db.add_column(u'oai_abstractmodel', 'ACMClass',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True),
                      keep_default=False)


        # Changing field 'AbstractModel.created'
        db.alter_column(u'oai_abstractmodel', 'created', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'AbstractModel.datestamp'
        db.alter_column(u'oai_abstractmodel', 'datestamp', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=15))

    def backwards(self, orm):
        # Adding field 'AbstractModel.mscClass'
        db.add_column(u'oai_abstractmodel', 'mscClass',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True),
                      keep_default=False)

        # Deleting field 'AbstractModel.MSCClass'
        db.delete_column(u'oai_abstractmodel', 'MSCClass')

        # Deleting field 'AbstractModel.ACMClass'
        db.delete_column(u'oai_abstractmodel', 'ACMClass')


        # Changing field 'AbstractModel.created'
        db.alter_column(u'oai_abstractmodel', 'created', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'AbstractModel.datestamp'
        db.alter_column(u'oai_abstractmodel', 'datestamp', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'AbstractModel.identifier'
        db.alter_column(u'oai_abstractmodel', 'identifier', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    models = {
        u'oai.abstractmodel': {
            'ACMClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'MSCClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "'[abstract]'"}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.TextField', [], {'default': "'[authors]'"}),
            'categories': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'datestamp': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'doi': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': "'[identifier]'", 'max_length': '15'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True'}),
            'rated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'[title]'", 'max_length': '300'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['oai']