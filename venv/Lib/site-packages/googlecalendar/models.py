import re
import urllib
from django.db import models
from django.db.models import Q
import gdata
import atom
import datetime
from django.db.models import Manager
from utils import parse_date_w3dtf, format_datetime, to_role_uri, from_role_uri
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


from feincms.models import Base
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent

import mptt
from incuna.db.models.AutoSlugField import AutoSlugField
from django.contrib.auth.models import User

VERSION = '0.3'

_services = {}

re_cal_id = re.compile(r".*/(.*)")


def with_request_error_try(function, attempts=3):
    """
    Attempt to call the function within a RequestError try / catch.
    """
    while True:
        try:
            return function()
        except gdata.service.RequestError, e:
            attempts -= 1
            if attempts == 0:
                raise
            if e.args[0]['status'] != 302:
                raise


class Account(models.Model):
    email = models.CharField(max_length = 100, blank = True)
    password = models.CharField(max_length = 100, blank = True)
    token = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        if self.email:
            return u'Account for %s' % self.email
        else:
            return u'Account with token'

    @property
    def service(self):
        if not _services.has_key(self.email):
            _service = gdata.calendar.service.CalendarService()
            _service.source = 'ITSLtd-Django_Google-%s' % VERSION
            if self.token:
                _service.auth_token = self.token
            else:
                _service.email = self.email
                _service.password = self.password
                _service.ProgrammaticLogin()
                _services[self.email] = _service
        return _services[self.email]

    def get_own_calendars(self, commit=True):
        cals = self.service.GetOwnCalendarsFeed()
        result = []
        for cal in cals.entry:
            result.append(Calendar.objects.from_gcal(self, cal, commit=commit))
        return result


class CalendarManager(Manager):
    def from_gcal(self, account, gcal, commit=True):
        uri = gcal.id.text
        try:
            instance = self.get(uri = uri)
        except self.model.DoesNotExist:
            instance = self.model(account=account, uri=uri)

        # copy attributes from gcal
        for prop in ['title', 'where', 'summary', 'color', 'timezone', ]:
            attr = getattr(gcal, prop)
            if hasattr(attr, 'value'):
                setattr(instance, prop, attr.value or '')
            elif hasattr(attr, 'text'):
                setattr(instance, prop, attr.text or '')

        for link in gcal.link:
            if link.rel == 'alternate':
                instance.feed_uri = link.href
                break

        # Default Acl
        rule = instance.getAclRule('default')
        instance.default_share = rule and from_role_uri(rule.role.value)


        if commit:
            instance.save()

        return instance


    def active(self):
        " Returns calendars available for current site only."
        current_site = Site.objects.get_current()
        return super(CalendarManager, self).get_queryset().filter(sites=current_site)

class ActiveManager(CalendarManager):
    def get_queryset(self):
        return self.active()


class Calendar(models.Model):
    SHARE_CHOICES = (
        ('freebusy', _('See only free / busy (hide details)')),
        ('read', _('See all event details')),
    )
    account = models.ForeignKey(Account)
    uri = models.CharField(max_length = 255, unique = True, editable=False, help_text=_('Google calendar address. Leave blank to create a Google calendar.'))
    calendar_id = models.CharField(max_length = 255, editable=False, unique = True)
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 255, help_text=_('This will be automatically generated from the  title'), unique=True)
    where = models.CharField(max_length = 100, blank = True, help_text=_('Location (e.g Oxford, UK).'))
    color = models.CharField(max_length = 10, blank = True, help_text=_('Leave blank to populate from Google.'))
    timezone = models.CharField(max_length = 100, blank = True, help_text=_('Leave blank to populate from Google.'))
    summary = models.TextField(blank=True, null=True)
    feed_uri = models.CharField(max_length = 255, blank = True, editable=False)

    default_share = models.CharField(_("Share with public"), max_length=31, blank = True, null = True, choices=SHARE_CHOICES, default=SHARE_CHOICES[1][0])

    sites = models.ManyToManyField(Site)

    objects = CalendarManager()
    active = ActiveManager()


    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('googlecalendar_detail', (), {
                'calendar': self.slug,
                })

    def save(self):
        gcal = self.gCalendar
        if gcal:
            # existing calendar update
            new = False
        else:
            new = True
            gcal = gdata.calendar.CalendarListEntry()

        gcal.title = atom.Title(text=self.title)
        gcal.summary = atom.Summary(text=self.summary)
        if self.where:
            gcal.where = gdata.calendar.Where(value_string=self.where)
        elif gcal.where and gcal.where.text:
            self.where = gcal.where.text
        if self.color:
            gcal.color = gdata.calendar.Color(value=self.color)
        elif gcal.color and gcal.color.value:
            self.color = gcal.color.value
        if self.timezone:
            gcal.timezone = gdata.calendar.Timezone(value=self.timezone)
        elif gcal.timezone and gcal.timezone.value:
            self.timezone = gcal.timezone.value

        if new:
            new_gcal = with_request_error_try(lambda: self.account.service.InsertCalendar(new_calendar=gcal))
            # gooogle replaces the title with the (email address) style Calendar Id
            #self.calendar_id = new_gcal.title.text
            new_gcal.title = atom.Title(text=self.title)
            new_gcal = self.account.service.UpdateCalendar(calendar=new_gcal)

            self.uri = new_gcal.id.text
            for link in new_gcal.link:
                if link.rel == 'alternate':
                    self.feed_uri = link.href
                    break

        else:
            new_gcal = with_request_error_try(lambda: self.account.service.UpdateCalendar(calendar=gcal))

        m = re_cal_id.match(self.uri)
        if m:
            self.calendar_id = urllib.unquote(m.group(1))

        # ACL model
        rule = self.getAclRule('default')
        if not self.default_share:
            # Not sharing
            if rule is not None:
                # remove the rule
                with_request_error_try(lambda: self.account.service.DeleteAclEntry(rule.GetEditLink().href))
        else:
            if rule is None:
                # new rule
                self.setAclRule(role=self.default_share, scope_type='default')
            elif to_role_uri(self.default_share) != rule.role.value:
                # role change
                self.setAclRule(rule=rule, role=self.default_share)


        super(Calendar, self).save()


    @property
    def upcoming_events(self):
        now = datetime.datetime.now()
        return self.event_set.filter(Q(start_time__gte=now) | Q(end_time__gte=now)).order_by('start_time')

    @property
    def gCalendar(self):
        if getattr(self, '_gCalendar', None):
            return self._gCalendar
        if self.uri:
            for c in self.account.service.GetOwnCalendarsFeed().entry:
                if self.uri == c.id.text:
                    self._gCalendar = c
                    return self._gCalendar

        return None

    def getAclRule(self, scope_type='default',):
        gcal = self.gCalendar
        if not gcal:
            return None
        aclink = gcal.GetAclLink()

        try:
            #try to get the entry
            return self.account.service.GetCalendarAclEntry('%s/%s' % (aclink.href, scope_type))
        except gdata.service.RequestError, e:
            if e.args[0]['reason'] != 'Not Found':
                raise
            return None


    def setAclRule(self, rule=None, role='read', scope_type='default', scope_value=None):
        """
        Set the role for a rule. If no rule is specified a new rule will be created with the provides scope_type / scope_type.
        """

        gcal = self.gCalendar
        if not gcal:
            return None
        aclink = gcal.GetAclLink()

        newRole = gdata.calendar.Role(value=to_role_uri(role))

        if rule is None:
            # add the entry
            rule = gdata.calendar.CalendarAclEntry()

            rule.scope = gdata.calendar.Scope()
            rule.scope.type = scope_type
            if scope_value:
                rule.scope.value = scope_value

            rule.role = newRole
            return with_request_error_try(lambda: self.account.service.InsertAclEntry(rule, aclink.href))
        else:
            # update the entry
            rule.role = newRole
            return with_request_error_try(lambda: self.account.service.UpdateAclEntry(rule.GetEditLink().href, rule))


    def get_events(self, commit=True):
        events = self.account.service.GetCalendarEventFeed(uri = self.feed_uri)
        result = []
        for i, event in enumerate(events.entry):
            result.append(Event.objects.from_gcal(self, event, commit=commit))
        return result


class EventManager(Manager):
    def from_gcal(self, calendar, data, commit=True):
        uri = data.id.text
        try:
            instance = self.get(uri = uri)
        except self.model.DoesNotExist:
            instance = self.model(calendar = calendar, uri = uri)

        instance.title = data.title.text or ''
        instance.summary = data.content.text or ''
        instance.start_time = parse_date_w3dtf(data.when[0].start_time)
        instance.end_time = parse_date_w3dtf(data.when[0].end_time)
        instance.edit_uri = data.GetEditLink().href
        instance.view_uri = data.GetHtmlLink().href

        if commit:
            instance.save()

        return instance

    def upcoming(self):
        """Current (and upcoming component)"""
        now = datetime.datetime.now()
        return self.active().filter(Q(start_time__gte=now) | Q(end_time__gte=now)).order_by('start_time')


    def active(self):
        " Returns events for those calendars that available for current site only."
        current_site = Site.objects.get_current()
        return super(EventManager, self).get_queryset().filter(calendar__sites=current_site, is_active=True)


class Event(Base):
    calendar = models.ForeignKey(Calendar)
    uri = models.CharField(max_length = 255, unique = True, editable=False)
    title = models.CharField(max_length = 255)
    slug = AutoSlugField(max_length = 255, populate_from='title', editable=True, help_text=_('This will be automatically generated from the  title'))
    edit_uri = models.CharField(max_length = 255, editable=False)
    view_uri = models.CharField(max_length = 255, editable=False)
    summary = models.TextField(blank = True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    user = models.ForeignKey(User, null=True)
    add_date = models.DateTimeField(_('Date added'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True, )

    objects = EventManager()

    class Meta:
        ordering = ('-start_time',)
        get_latest_by = 'start_time'
        unique_together = ('calendar', 'slug')

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('googlecalendar_event', (), {
                'slug': self.calendar.slug,
                'event': self.slug,
                })

    def save(self):

        self._meta.get_field('slug').pre_save(self, not self.pk)

        content = self.summary
        content += """<p><a target="_top" href="%s%s">Full event details</a></p>""" % (Site.objects.get_current().domain, self.get_absolute_url(), )

        if self.uri:
            # existing event, update
            entry = self.calendar.account.service.GetCalendarEventEntry(uri = self.edit_uri)
            entry.title.text = self.title
            entry.content.text = content
            start_time = format_datetime(self.start_time)
            end_time = format_datetime(self.end_time)
            entry.when = []
            entry.when.append(gdata.calendar.When(start_time = start_time, end_time = end_time))
            new_entry = with_request_error_try(lambda: self.calendar.account.service.UpdateEvent(entry.GetEditLink().href, entry))
        else:
            entry = gdata.calendar.CalendarEventEntry()
            entry.title = atom.Title(text = self.title)
            entry.content = atom.Content(text = content)
            if not self.start_time:
                self.start_time = datetime.datetime.utcnow()
            if not self.end_time:
                self.end_time = self.start_time + datetime.timedelta(hours = 1)
            start_time = format_datetime(self.start_time)
            end_time = format_datetime(self.end_time)
            entry.when.append(gdata.calendar.When(start_time = start_time, end_time = end_time))
            new_entry = with_request_error_try(lambda: self.calendar.account.service.InsertEvent(entry, self.calendar.feed_uri))
            self.uri = new_entry.id.text
            self.edit_uri = new_entry.GetEditLink().href
            self.view_uri = new_entry.GetHtmlLink().href

        super(Event, self).save()

    def delete(self):
        if self.uri:
            try:
                # existing event, delete
                self.calendar.account.service.DeleteEvent(self.edit_uri)
            except gdata.service.RequestError, e:
                if e.args[0]['status'] != 404:
                    raise
        super(Event, self).delete()
