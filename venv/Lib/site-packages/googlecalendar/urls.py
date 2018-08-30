from django.conf.urls import patterns, url

urlpatterns = patterns('googlecalendar.views',
    url(r'^(?P<slug>[a-z0-9_-]+)/(?P<event>[a-z0-9_-]+)$', 'googlecalendar_event', name='googlecalendar_event'),
    url(r'^(?P<slug>[a-z0-9_-]+)/$', 'googlecalendar', name='googlecalendar_detail'),
    url(r'^$', 'googlecalendar_list', name='googlecalendar'),
)

