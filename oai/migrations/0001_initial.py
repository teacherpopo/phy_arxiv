# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryModel'
        db.create_table(u'oai_categorymodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abstract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oai.AbstractModel'])),
        ))
        db.send_create_signal(u'oai', ['CategoryModel'])

        # Adding model 'AuthorModel'
        db.create_table(u'oai_authormodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('forenames', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abstract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oai.AbstractModel'])),
        ))
        db.send_create_signal(u'oai', ['AuthorModel'])

        # Adding model 'AbstractModel'
        db.create_table(u'oai_abstractmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datestamp', self.gf('django.db.models.fields.DateField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('licenseStr', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('abstract', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateField')(null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
            ('journalRef', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'oai', ['AbstractModel'])


    def backwards(self, orm):
        # Deleting model 'CategoryModel'
        db.delete_table(u'oai_categorymodel')

        # Deleting model 'AuthorModel'
        db.delete_table(u'oai_authormodel')

        # Deleting model 'AbstractModel'
        db.delete_table(u'oai_abstractmodel')


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
        },
        u'oai.authormodel': {
            'Meta': {'object_name': 'AuthorModel'},
            'abstract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oai.AbstractModel']"}),
            'forenames': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'oai.categorymodel': {
            'Meta': {'object_name': 'CategoryModel'},
            'abstract': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oai.AbstractModel']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['oai']