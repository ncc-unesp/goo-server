# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserToken'
        db.create_table('core_usertoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['UserToken'])

        # Adding model 'UserProfile'
        db.create_table('core_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('core', ['UserProfile'])

        # Adding model 'Application'
        db.create_table('core_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_version', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('_description', self.gf('django.db.models.fields.TextField')(default='')),
            ('_usage', self.gf('django.db.models.fields.TextField')(default='')),
            ('_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('executable', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('_app_obj', self.gf('django.db.models.fields.related.ForeignKey')(related_name='application_set', null=True, to=orm['storage.Object'])),
            ('args', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('inputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('outputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('checkpoints', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('_multi_hosts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_multi_thread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_shared_fs', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_constant_fields', self.gf('django.db.models.fields.CharField')(default='', max_length=1024)),
            ('_required_fields', self.gf('django.db.models.fields.CharField')(default='', max_length=1024)),
            ('hosts', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('cores_per_host', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('maxtime', self.gf('django.db.models.fields.PositiveIntegerField')(default=43200)),
            ('diskspace', self.gf('django.db.models.fields.PositiveIntegerField')(default=2048)),
            ('memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2048)),
        ))
        db.send_create_signal('core', ['Application'])

        # Adding model 'Job'
        db.create_table('core_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Application'])),
            ('progress', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('hosts', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('cores_per_host', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('restart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('executable', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('args', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('inputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('outputs', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('checkpoints', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('maxtime', self.gf('django.db.models.fields.PositiveIntegerField')(default=43200)),
            ('diskspace', self.gf('django.db.models.fields.PositiveIntegerField')(default=2048)),
            ('memory', self.gf('django.db.models.fields.PositiveIntegerField')(default=2048)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('diskspace_in_use', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('memory_in_use', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('progress_string', self.gf('django.db.models.fields.TextField')(default='')),
            ('eta', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('return_code', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('pilot', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['dispatcher.Pilot'], null=True)),
        ))
        db.send_create_signal('core', ['Job'])

        # Adding M2M table for field input_objs on 'Job'
        db.create_table('core_job_input_objs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['core.job'], null=False)),
            ('object', models.ForeignKey(orm['storage.object'], null=False))
        ))
        db.create_unique('core_job_input_objs', ['job_id', 'object_id'])

        # Adding M2M table for field output_objs on 'Job'
        db.create_table('core_job_output_objs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['core.job'], null=False)),
            ('object', models.ForeignKey(orm['storage.object'], null=False))
        ))
        db.create_unique('core_job_output_objs', ['job_id', 'object_id'])

        # Adding M2M table for field checkpoint_objs on 'Job'
        db.create_table('core_job_checkpoint_objs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['core.job'], null=False)),
            ('object', models.ForeignKey(orm['storage.object'], null=False))
        ))
        db.create_unique('core_job_checkpoint_objs', ['job_id', 'object_id'])

        # Adding M2M table for field parent on 'Job'
        db.create_table('core_job_parent', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_job', models.ForeignKey(orm['core.job'], null=False)),
            ('to_job', models.ForeignKey(orm['core.job'], null=False))
        ))
        db.create_unique('core_job_parent', ['from_job_id', 'to_job_id'])


    def backwards(self, orm):
        # Deleting model 'UserToken'
        db.delete_table('core_usertoken')

        # Deleting model 'UserProfile'
        db.delete_table('core_userprofile')

        # Deleting model 'Application'
        db.delete_table('core_application')

        # Deleting model 'Job'
        db.delete_table('core_job')

        # Removing M2M table for field input_objs on 'Job'
        db.delete_table('core_job_input_objs')

        # Removing M2M table for field output_objs on 'Job'
        db.delete_table('core_job_output_objs')

        # Removing M2M table for field checkpoint_objs on 'Job'
        db.delete_table('core_job_checkpoint_objs')

        # Removing M2M table for field parent on 'Job'
        db.delete_table('core_job_parent')


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
            '_app_obj': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'application_set'", 'null': 'True', 'to': "orm['storage.Object']"}),
            '_constant_fields': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            '_description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_multi_hosts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_multi_thread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            '_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_required_fields': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            '_shared_fs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_usage': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_version': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'args': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'cores_per_host': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'diskspace': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'hosts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'maxtime': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'outputs': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'core.job': {
            'Meta': {'object_name': 'Job'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Application']"}),
            'args': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'checkpoint_objs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'checkpoint_for'", 'null': 'True', 'to': "orm['storage.Object']"}),
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'cores_per_host': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diskspace': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'diskspace_in_use': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'eta': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'hosts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_objs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'input_for'", 'null': 'True', 'to': "orm['storage.Object']"}),
            'inputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'maxtime': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'memory': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2048'}),
            'memory_in_use': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'output_objs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'output_for'", 'null': 'True', 'to': "orm['storage.Object']"}),
            'outputs': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Job']", 'symmetrical': 'False'}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['dispatcher.Pilot']", 'null': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'progress_string': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'restart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'return_code': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        },
        'storage.object': {
            'Meta': {'object_name': 'Object'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_type': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['core']