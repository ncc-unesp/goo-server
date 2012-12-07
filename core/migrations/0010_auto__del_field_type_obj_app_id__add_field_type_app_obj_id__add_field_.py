# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Type.obj_app_id'
        db.delete_column('core_type', 'obj_app_id')

        # Adding field 'Type.app_obj_id'
        db.add_column('core_type', 'app_obj_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.executable'
        db.add_column('core_job', 'executable',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.args'
        db.add_column('core_job', 'args',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.inputs'
        db.add_column('core_job', 'inputs',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.outputs'
        db.add_column('core_job', 'outputs',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.checkpoints'
        db.add_column('core_job', 'checkpoints',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Job.app_obj_id'
        db.add_column('core_job', 'app_obj_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Type.obj_app_id'
        db.add_column('core_type', 'obj_app_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Deleting field 'Type.app_obj_id'
        db.delete_column('core_type', 'app_obj_id')

        # Deleting field 'Job.executable'
        db.delete_column('core_job', 'executable')

        # Deleting field 'Job.args'
        db.delete_column('core_job', 'args')

        # Deleting field 'Job.inputs'
        db.delete_column('core_job', 'inputs')

        # Deleting field 'Job.outputs'
        db.delete_column('core_job', 'outputs')

        # Deleting field 'Job.checkpoints'
        db.delete_column('core_job', 'checkpoints')

        # Deleting field 'Job.app_obj_id'
        db.delete_column('core_job', 'app_obj_id')


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
            'app_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'args': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'checkpoing_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disk_in_use': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'disk_requirement': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'eta': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'hosts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'inputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'memory_in_use': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'memory_requirement': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'output_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'outputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['dispatcher.Pilot']", 'null': 'True'}),
            'pph': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'restart': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'return_code': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'ttl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Type']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.type': {
            'Meta': {'object_name': 'Type'},
            'app_obj_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'args': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'multi_hosts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'multi_thread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'outputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'shared_fs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Version']"})
        },
        'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core.usertoken': {
            'Meta': {'object_name': 'UserToken'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.version': {
            'Meta': {'object_name': 'Version'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'dispatcher.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'cores': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dispatcher.Site']"}),
            'threads': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'dispatcher.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_cores': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'max_threads': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'max_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['core']