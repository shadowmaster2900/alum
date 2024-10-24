# admin_ip_middleware.py

from django.http import HttpResponseForbidden
from alumni.models import IPWhiteList

class AdminIPMiddleware:
    """ Middleware to restrict access to admin page based on IP addresses """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Define your allowed IP addresses

        
        # Check if the user's IP is whitelisted
        
        # Continue processing the request
        response = self.get_response(request)
        return response
