# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AbstractCacheModel'
        db.create_table(u'oai_abstractcachemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datestamp', self.gf('django.db.models.fields.DateField')(default=None, null=True, db_index=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, null=True)),
            ('created', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('authors', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('categories', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('licenseStr', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('journalRef', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('reportNo', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('rated', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('archive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('MSCClass', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('ACMClass', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
        ))
        db.send_create_signal(u'oai', ['AbstractCacheModel'])

        # Adding model 'AbstractModel'
        db.create_table(u'oai_abstractmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datestamp', self.gf('django.db.models.fields.DateField')(default=None, null=True, db_index=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, null=True)),
            ('created', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('authors', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('categories', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('licenseStr', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('journalRef', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True)),
            ('reportNo', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('rated', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('archived', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('MSCClass', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('ACMClass', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('cached', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'oai', ['AbstractModel'])


    def backwards(self, orm):
        # Deleting model 'AbstractCacheModel'
        db.delete_table(u'oai_abstractcachemodel')

        # Deleting model 'AbstractModel'
        db.delete_table(u'oai_abstractmodel')


    models = {
        u'oai.abstractcachemodel': {
            'ACMClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'MSCClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'Meta': {'object_name': 'AbstractCacheModel'},
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
        },
        u'oai.abstractmodel': {
            'ACMClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'MSCClass': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'Meta': {'object_name': 'AbstractModel'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'archived': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'authors': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'cached': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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