# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Site.max_threads'
        db.delete_column('dispatcher_site', 'max_threads')

        # Adding field 'Site.max_hosts'
        db.add_column('dispatcher_site', 'max_hosts',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Pilot.threads'
        db.delete_column('dispatcher_pilot', 'threads')

        # Adding field 'Pilot.hosts'
        db.add_column('dispatcher_pilot', 'hosts',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Site.max_threads'
        db.add_column('dispatcher_site', 'max_threads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Site.max_hosts'
        db.delete_column('dispatcher_site', 'max_hosts')

        # Adding field 'Pilot.threads'
        db.add_column('dispatcher_pilot', 'threads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Pilot.hosts'
        db.delete_column('dispatcher_pilot', 'hosts')


    models = {
        'dispatcher.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'cores': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hosts': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dispatcher.Site']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'dispatcher.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_cores': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'max_hosts': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'max_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['dispatcher']