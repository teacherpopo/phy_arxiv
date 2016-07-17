# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AuthorModel'
        db.delete_table(u'oai_authormodel')

        # Deleting model 'CategoryModel'
        db.delete_table(u'oai_categorymodel')


    def backwards(self, orm):
        # Adding model 'AuthorModel'
        db.create_table(u'oai_authormodel', (
            ('abstract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oai.AbstractModel'])),
            ('keyname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forenames', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'oai', ['AuthorModel'])

        # Adding model 'CategoryModel'
        db.create_table(u'oai_categorymodel', (
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abstract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oai.AbstractModel'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'oai', ['CategoryModel'])


    models = {
        u'oai.abstractmodel': {
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'datestamp': ('django.db.models.fields.DateField', [], {}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'journalRef': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'licenseStr': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateField', [], {'null': 'True'})
        }
    }

    complete_apps = ['oai']