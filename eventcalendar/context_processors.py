# context_processors.py
from alumni.models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipients=request.user).order_by('-timestamp')
        unread_notifications = notifications.exclude(read_by=request.user)
    else:
        unread_notifications = None
    return {'unread_notifications': unread_notifications}
