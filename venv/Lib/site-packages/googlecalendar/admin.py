from django.contrib import admin
from django import forms
from models import *
from incunafein.admin import editor
from django.conf import settings

class CalendarAdmin(admin.ModelAdmin):
    list_display = ['title', 'calendar_id', ]
    list_filter = ( 'account',)
    search_fields = ('title', 'slug', 'summary',)
    prepopulated_fields = {
        'slug': ('title',),
        }


class EventAdmin(editor.ItemEditor, admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ('__unicode__', 'calendar', 'start_time', 'end_time',)
    list_filter = ( 'calendar',)
    search_fields = ('title', 'slug', 'summary',)
    prepopulated_fields = {
        'slug': ('title',),
        }
    actions = ['delete_selected', ]
    readonly_fields = ['user',]
    verbose_name_plural = 'Events'

    if hasattr(settings, 'TINYMCE_JS_URL'):
        # If available add TINYMCE (assumes settings.STATIC_URL+'scripts/tiny_init.js' is present)
        class Media:
            js = (settings.TINYMCE_JS_URL, settings.STATIC_URL+'scripts/tiny_init.js',)
    

    # override the default delete action to ensure that the event in the google calendar is also deleteed 
    def delete_selected(self, request, queryset):
        for e in queryset:
            e.delete()
    delete_selected.short_description = "Delete selected events!"


admin.site.register(Account)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)

