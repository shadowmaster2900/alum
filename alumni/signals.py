# alumni/signals.py

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from calendarapp.models import Event  # Import the Event model from your app
from django.contrib.auth.signals import user_logged_in
from alumni.utils import generate_notifications_for_upcoming_events

from .models import Alumni

@receiver(pre_delete, sender=Alumni)
def delete_related_events(sender, instance, **kwargs):
    # Delete all events related to the deleted alumni
    Event.objects.filter(title=f"{instance.name}'s Birthday").delete()

@receiver(user_logged_in)
def generate_notifications_on_login(sender, request, user, **kwargs):
    generate_notifications_for_upcoming_events(user)