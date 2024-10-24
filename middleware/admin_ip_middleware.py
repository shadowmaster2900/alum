# admin_ip_middleware.py

from django.http import HttpResponseForbidden
from alumni.models import IPWhiteList

class AdminIPMiddleware:
    """ Middleware to restrict access to admin page based on IP addresses """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Define your allowed IP addresses
        ALLOWED_IPS =  list(IPWhiteList.objects.values_list('ip_address', flat=True)) + [
            "127.0.0.1", "104.12.136.249", '87.208.43.160','164.68.122.101', 
            '73.154.43.139', '93.125.107.20', '84.241.196.145', 
            '84.241.201.175', '144.91.119.150', '67.172.58.14', 
            '93.125.107.23', '3.67.6.29'
        ]

        print(f"THIS GUY IS TRYING TO GET INTO ADMIN: {user_ip}")
        
        # Get the user's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        
        # Check if the user's IP is whitelisted
        
        # Continue processing the request
        response = self.get_response(request)
        return response
