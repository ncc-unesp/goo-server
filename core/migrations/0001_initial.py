# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table('core_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('core', ['Application'])

        # Adding model 'Version'
        db.create_table('core_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'])),
        ))
        db.send_create_signal('core', ['Version'])

        # Adding model 'Type'
        db.create_table('core_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Version'])),
            ('executable', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('obj_app_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('args', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('inputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('outputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('checkpoints', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('multi_hosts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('multi_thread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('shared_fs', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('core', ['Type'])

        # Adding model 'Job'
        db.create_table('core_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Version'])),
            ('progress', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hosts', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pph', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('restart', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('input_obj_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('output_obj_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('checkpoing_obj_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('ttl', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('disk_requirement', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('memory_requirement', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('disk_in_use', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('memory_in_use', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('eta', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('return_code', self.gf('django.db.models.fields.IntegerField')()),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['Job'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table('core_application')

        # Deleting model 'Version'
        db.delete_table('core_version')

        # Deleting model 'Type'
        db.delete_table('core_type')

        # Deleting model 'Job'
        db.delete_table('core_job')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.application': {
            'Meta': {'object_name': 'Application'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.job': {
            'Meta': {'object_name': 'Job'},
            'checkpoing_obj_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'disk_in_use': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'disk_requirement': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'eta': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hosts': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_obj_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'memory_in_use': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'memory_requirement': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'output_obj_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'pph': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'progress': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'restart': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'return_code': ('django.db.models.fields.IntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Version']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.type': {
            'Meta': {'object_name': 'Type'},
            'args': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'multi_hosts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'multi_thread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'obj_app_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'outputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'shared_fs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Version']"})
        },
        'core.version': {
            'Meta': {'object_name': 'Version'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['core']