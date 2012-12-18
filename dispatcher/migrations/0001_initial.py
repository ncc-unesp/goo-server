# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table('dispatcher_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('max_cores', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('max_hosts', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('max_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('dispatcher', ['Site'])

        # Adding model 'Pilot'
        db.create_table('dispatcher_pilot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatcher.Site'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('cores', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hosts', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('memory', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('dispatcher', ['Pilot'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table('dispatcher_site')

        # Deleting model 'Pilot'
        db.delete_table('dispatcher_pilot')


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