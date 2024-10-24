from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from alumni.models import Notification
from django.shortcuts import render, redirect


from calendarapp.models import Event
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')




class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(recipients=request.user).order_by('-timestamp')
        unread_notifications = notifications.exclude(read_by=request.user)
        read_notifications = notifications.filter(read_by=request.user)[:10]

        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "notifications": notifications,
            "unread_notifications": unread_notifications,
            "read_notifications": read_notifications,
        }
        return render(request, self.template_name, context)
