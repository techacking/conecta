# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Event.user'
        db.add_column('googlecalendar_event', 'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True), keep_default=False)

        # Adding field 'Event.add_date'
        db.add_column('googlecalendar_event', 'add_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2010, 12, 14, 14, 49, 51, 749206), blank=True), keep_default=False)

        # Adding field 'Event.is_active'
        db.add_column('googlecalendar_event', 'is_active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding M2M table for field sites on 'Calendar'
        db.create_table('googlecalendar_calendar_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('calendar', models.ForeignKey(orm['googlecalendar.calendar'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('googlecalendar_calendar_sites', ['calendar_id', 'site_id'])


    def backwards(self, orm):
        
        # Deleting field 'Event.user'
        db.delete_column('googlecalendar_event', 'user_id')

        # Deleting field 'Event.add_date'
        db.delete_column('googlecalendar_event', 'add_date')

        # Deleting field 'Event.is_active'
        db.delete_column('googlecalendar_event', 'is_active')

        # Removing M2M table for field sites on 'Calendar'
        db.delete_table('googlecalendar_calendar_sites')


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
        'googlecalendar.account': {
            'Meta': {'object_name': 'Account'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'googlecalendar.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['googlecalendar.Account']"}),
            'calendar_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'default_share': ('django.db.models.fields.CharField', [], {'default': "'read'", 'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'feed_uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'googlecalendar.event': {
            'Meta': {'ordering': "('-start_time',)", 'unique_together': "(('calendar', 'slug'),)", 'object_name': 'Event'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['googlecalendar.Calendar']"}),
            'edit_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('incuna.db.models.AutoSlugField.AutoSlugField', [], {'db_index': 'True', 'max_length': '255', 'populate_from': "'title'", 'field_separator': "u'-'"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'view_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'googlecalendar.mediafilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'MediaFileContent', 'db_table': "'googlecalendar_event_mediafilecontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediafile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'googlecalendar_mediafilecontent_set'", 'to': "orm['medialibrary.MediaFile']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafilecontent_set'", 'to': "orm['googlecalendar.Event']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'googlecalendar.richtextcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContent', 'db_table': "'googlecalendar_event_richtextcontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontent_set'", 'to': "orm['googlecalendar.Event']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'medialibrary.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['googlecalendar']
