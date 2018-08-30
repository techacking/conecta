import urllib
import itertools
from django.conf import settings
from django import template 
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from googlecalendar.utils import request_single_token
from googlecalendar.models import Calendar, Event

GOOGLECALENDAR_DEFAULTS = dict(
    # iframe attributes 
    style=" border-width:0 ", 
    width="800",
    height="600", 
    frameborder="0", 
    scrolling="no",
    # Calender attributes
    showTitle="0", 
    showCalendars="1", 
    showTz="0", 
    wkst="1", 
    bgcolor="#FFFFFF", 
    ctz="Europe/London")

IFRAME_ATTRS = (
    'style',
    'width',
    'height',
    'frameborder',
    'scrolling',
    'longdesc',
    'marginheight',
    'marginwidth',
)

if hasattr(settings, 'GOOGLECALENDAR_DEFAULTS'):
    GOOGLECALENDAR_DEFAULTS.update(settings.GOOGLECALENDAR_DEFAULTS)

register = template.Library()

class GoogleCalendarAuthNode(template.Node):
	def __init__(self, uri):
		self.uri = uri
	def render(self, context):
		uri = template.resolve_variable(self.uri, context)
		return request_single_token(uri)

@register.tag
def google_calendar_auth(parser, token):
	bits = token.contents.split()
	len_bits = len(bits)
	if len_bits != 2:
		raise template.TemplateSyntaxError('%s tag requires URI as an argument' % bits[0])
	return GoogleCalendarAuthNode(bits[1])


class CalendarNode(template.Node):
    """
        Render a google calendar (iframe) embed.

        Usage:
            {% calendar %}
            {% calendar 'joe@gmail.com' %}
            {% calendar 'joe@gmail.com' width="580" height="350" %}
            {% calendar 'joe@gmail.com' 'james@gmail.com' width="580" height="350" %}
            {% calendar 'joe@gmail.com' 'james@gmail.com' calendar_instance width="580" height="350" %}
    """

    COLOURS = ['#D96666', '#E67399', '#8C66D9', '#668CB3', '#668CD9', '#59BFB3', '#65AD89', '#4CB052', '#8CBF40', '#E0C240',
               '#E6804D', '#BE9494', '#A992A9', '#8997A5', '#94A2BE', '#85AAA5', '#A7A77D', '#C4A883', '#C7561E', '#B5515D',
               '#C244AB', '#603F99', '#536CA6', '#3640AD', '#3C995B', '#5CA632', '#7EC225', '#A7B828', '#CF9911', '#D47F1E',
               '#B56414', '#914D14', '#AB2671', '#9643A5', '#4585A3', '#737373', '#41A587', '#D1BC36', '#AD2D2D', ]

    @staticmethod
    def colours(start = 0):
        """
        Returns a stream of colours, if the end of the list is reached then it starts back at the beginning.
        """
        while True:
            try:
                yield CalendarNode.COLOURS[start]
            except IndexError:
                start = 0
                yield CalendarNode.COLOURS[start]
            start += 1

    def __init__(self, *args, **kwargs):
        self.calendars = args
        self.attrs = kwargs

    def render(self, context):

        iframe_attrs = {}
        calendar_attrs = {}
        for key, value in GOOGLECALENDAR_DEFAULTS.items():
            if key in IFRAME_ATTRS:
                iframe_attrs[key] = value
            else:
                calendar_attrs[key] = value



        if not self.calendars:
            calendars = Calendar.objects.active()
        else:
            calendars = []
            def add_calendars(cals):
               for cal in cals:

                   if isinstance(cal, basestring):
                       try:
                           cal = Calendar.objects.active().get(calendar_id=cal)
                       except Calendar.DoesNotExist:
                           continue
                   elif getattr(cal, '__iter__', False):#isinstance(cal, (list, tuple)):
                       add_calendars(cal)
                       continue

                   calendars.append(cal)

            add_calendars([cal.resolve(context) for cal in self.calendars])

        if not calendars:
            return ''

        for key in self.attrs:
            value = self.attrs[key].resolve(context) or self.attrs[key]
            if key in IFRAME_ATTRS:
                iframe_attrs[key] = value
            else:
                calendar_attrs[key] = value

        colours = self.colours()
        src = "https://www.google.com/calendar/embed?%s" % ( '&'.join(["%s=%s" % (k, urllib.quote(v)) for k, v in calendar_attrs.items()]) )
        for calendar in calendars:
            src += "&src=%s&color=%s" % tuple(map(urllib.quote, (calendar.calendar_id, calendar.color or colours.next())))

        iframe_attrs['src'] = src

        return mark_safe(u'<iframe%s ></iframe>' % flatatt(iframe_attrs))

@register.tag()
def embedcalendar(parser, token):
    bits = token.split_contents() 

    calendars = []
    dict = {}
    try:
        for bit in bits[1:]:
            try:
                bit.index('=')
            except ValueError:
                calendars.append(parser.compile_filter(bit))
            else:
                pair = bit.split('=')
                dict[str(pair[0])] = parser.compile_filter(pair[1])
    except TypeError:
        raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % bits[0])

    return CalendarNode(*calendars, **dict)


class CalendarEventsNode(template.Node):
    """

    """
    def __init__(self, calendars=None, limit=None, varname=None):
        self.calendars = calendars
        self.limit = limit
        self.varname = varname

    def render(self, context):
        calendars = self.calendars and self.calendars.resolve(context)
        limit = self.limit and self.limit.resolve(context)


        events = Event.objects.upcoming()

        if calendars is None:
            pass
        elif isinstance(calendars, (str,unicode,)):
            try:
                calendars = [Calendar.objects.active().get(slug=calendars)]
            except Calendar.DoesNotExist:
                calendars = None

        elif not getattr(calendars, '__iter__', False):
            calendars = [calendars]


        if calendars is not None:
            events = events.filter(calendar__in=calendars)

        if limit is not None:
            events = events[:limit]

        if self.varname is not None:
            context[self.varname] = events
            return ''
        else:
            t = template.loader.select_template(['googlecalendar/events.html'])
            context.push()
            context['calendars'] = calendars
            context['events'] = events
            output = t.render(context)
            context.pop()

            return output


@register.tag()
def calendarevents(parser, token):
    bits = token.split_contents() 

    if bits[-2] == 'as':
        varname = bits[-1]
        args = bits[1:-2]
    else:
        args = bits[1:]
        varname = None

    return CalendarEventsNode(*map(parser.compile_filter, args), varname=varname)

