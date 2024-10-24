from django.views.generic import ListView

from calendarapp.models import Event
from alumni.models import BaseCalendarEvent

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        # Query both regular events and base calendar events
        regular_events = Event.objects.get_all_events(user=self.request.user)
        base_calendar_events = BaseCalendarEvent.objects.all()

        # Combine both event sets
        all_events = list(regular_events) + list(base_calendar_events)

        return all_events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_all'] = 'yes'
        context['all_events'] = self.get_queryset()  # Pass the all_events queryset to the context
        return context

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        events = Event.objects.get_running_events(user=self.request.user)
        
        return events 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_all'] = 'no'
        context['object_list'] = self.get_queryset()  # Pass the all_events queryset to the context
        return context
