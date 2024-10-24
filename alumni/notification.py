from django.utils import timezone
from datetime import timedelta
from .models import Event, Notification

def generate_upcoming_event_notifications():
    # Define the threshold for upcoming events (e.g., 7 days from now)
    threshold_date = timezone.now() + timedelta(days=7)
    
    # Query upcoming events that haven't been notified
    upcoming_events = Event.objects.filter(
        start_datetime__lte=threshold_date,
        notified=False  # Assuming you have a field in your Event model to track notifications
    )
    
    # Loop through upcoming events and generate notifications for users
    for event in upcoming_events:
        users_attending = event.attendees.all()  # Assuming you have a related field for attendees
        for user in users_attending:
            # Create a reminder notification for the user about the upcoming event
            message = f"Reminder: Upcoming Event - {event.title} on {event.start_datetime.strftime('%Y-%m-%d %H:%M')}"
            notification = Notification.objects.create(message=message, recipient=user)
            notification.save()
            
            # Mark the event as notified to prevent duplicate notifications
            event.notified = True
            event.save()

# You can call this function periodically, e.g., using a management command or a scheduled task.
