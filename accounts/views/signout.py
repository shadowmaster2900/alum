from django.shortcuts import redirect
from django.contrib.auth import logout
from alumni.models import UserAction


def signout(request):
    action_description = f"{request.user} logged out."
    UserAction.objects.create(
        user=request.user,  # User who performed the action
        action=action_description,  # Description of the action
    )
    logout(request)
    return redirect("accounts:signin")
