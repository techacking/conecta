from datetime import datetime

from django import forms
from django.utils.formats import localize_input
from django.utils.translation import ugettext_lazy as _

from googlecalendar.models import Event, Calendar

def get_current_time():
    return localize_input(datetime.now().strftime('%Y-%m-%d %I:%M'))

class AddEventForm(forms.ModelForm):
    """ Add event form for calendar_list page """
    calendar = forms.ModelChoiceField(queryset=Calendar.active)
    start_time = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(), label=_('Start date and time'), help_text=_('e.g. %s' % get_current_time()))
    end_time = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(), label=_('End date and time'), help_text=_('e.g. %s' % get_current_time()))

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time < start_time:
            raise forms.ValidationError("End date can not be earlier than start date.")
        return end_time

    class Meta:
        model = Event
        fields = ('calendar', 'title', 'summary', 'start_time', 'end_time')

class AddEventCalendarForm(AddEventForm):
    """ Add event form for calendar page. Calendar is preset. """

    def __init__(self, *args, **kwargs):
        self.calendar = kwargs.pop('calendar')
        super(AddEventCalendarForm, self).__init__(*args, **kwargs)
        self.fields['calendar'].widget=forms.HiddenInput()
        self.fields['calendar'].initial=self.calendar

