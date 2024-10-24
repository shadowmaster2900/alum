# context_processors.py
from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications_queryset = Notification.objects.filter(recipients=request.user).order_by('-timestamp')
        unread_notifications = notifications_queryset.filter(read_by=request.user)
    else:
        unread_notifications = None
    return {'notifications': unread_notifications}
