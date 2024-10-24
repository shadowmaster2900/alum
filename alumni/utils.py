from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, Event

def generate_notifications_for_upcoming_events(user):
    # Calculate the date three days from now
    three_days_from_now = timezone.now() + timedelta(days=2)
    
    # Query events happening three days from now
    upcoming_events = Event.objects.filter(start_time=three_days_from_now.date(), user=user)
    
    # Create notifications for each upcoming event
    for event in upcoming_events:
        message = f"Upcoming Event: {event.title} on {event.start_time}"
        
        # Create the notification and set the timestamp field to the current time
        notification = Notification(message=message, timestamp=timezone.now())
        notification.save()

        notification.recipients.add(user)
        notification.save()


# alumni/utils.py

from datetime import date
from django.core.mail import send_mail
from .models import Alumni

def send_birthday_emails():
    today = date.today()
    print(today)
    alumni_with_birthday = Alumni.objects.filter(birthday__day=today.day, birthday__month=today.month)

    if alumni_with_birthday:
        # Compose and send the birthday email
        subject = 'Birthday Greetings!'
        message = 'Happy Birthday to the following alumni:\n'
        for alumni in alumni_with_birthday:
            message += f'- {alumni.name} ({alumni.birthday})\n'

        from_email = 'meklek20@email.com'
        admin_email = 'mekgel80@email.com'
        send_mail(
            subject,
            message,
            "meklek20@gmail.com",
            ["mekgel80@gmail.com"],
            fail_silently=False,
        )

        return f'Birthday email sent to admin for {len(alumni_with_birthday)} alumni.'
    else:
        return 'No birthdays today.'


