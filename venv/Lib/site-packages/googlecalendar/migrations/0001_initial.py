# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('googlecalendar_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('googlecalendar', ['Account'])

        # Adding model 'Calendar'
        db.create_table('googlecalendar_calendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['googlecalendar.Account'])),
            ('uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('calendar_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('where', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('feed_uri', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('default_share', self.gf('django.db.models.fields.CharField')(default='read', max_length=31, null=True, blank=True)),
        ))
        db.send_create_signal('googlecalendar', ['Calendar'])

        # Adding model 'Event'
        db.create_table('googlecalendar_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['googlecalendar.Calendar'])),
            ('uri', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('incuna.db.models.AutoSlugField.AutoSlugField')(db_index=True, max_length=255, populate_from='title', field_separator=u'-')),
            ('edit_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('view_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('googlecalendar', ['Event'])

        # Adding unique constraint on 'Event', fields ['calendar', 'slug']
        db.create_unique('googlecalendar_event', ['calendar_id', 'slug'])

        # Adding model 'RichTextContent'
        db.create_table('googlecalendar_event_richtextcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontent_set', to=orm['googlecalendar.Event'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('googlecalendar', ['RichTextContent'])

        # Adding model 'MediaFileContent'
        db.create_table('googlecalendar_event_mediafilecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mediafilecontent_set', to=orm['googlecalendar.Event'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mediafile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='googlecalendar_mediafilecontent_set', to=orm['medialibrary.MediaFile'])),
            ('position', self.gf('django.db.models.fields.CharField')(default='default', max_length=10)),
        ))
        db.send_create_signal('googlecalendar', ['MediaFileContent'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Event', fields ['calendar', 'slug']
        db.delete_unique('googlecalendar_event', ['calendar_id', 'slug'])

        # Deleting model 'Account'
        db.delete_table('googlecalendar_account')

        # Deleting model 'Calendar'
        db.delete_table('googlecalendar_calendar')

        # Deleting model 'Event'
        db.delete_table('googlecalendar_event')

        # Deleting model 'RichTextContent'
        db.delete_table('googlecalendar_event_richtextcontent')

        # Deleting model 'MediaFileContent'
        db.delete_table('googlecalendar_event_mediafilecontent')


    models = {
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'googlecalendar.event': {
            'Meta': {'ordering': "('-start_time',)", 'unique_together': "(('calendar', 'slug'),)", 'object_name': 'Event'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['googlecalendar.Calendar']"}),
            'edit_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('incuna.db.models.AutoSlugField.AutoSlugField', [], {'db_index': 'True', 'max_length': '255', 'populate_from': "'title'", 'field_separator': "u'-'"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
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
        }
    }

    complete_apps = ['googlecalendar']
