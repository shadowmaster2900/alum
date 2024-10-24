from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from alumni.models import UserAction
from accounts.utils import send_otp
from datetime import datetime
import pyotp
import base64
from django_otp.plugins.otp_totp.models import TOTPDevice
from alumni.models import IPWhiteList

from accounts.forms import SignInForm

from alumni.utils import generate_notifications_for_upcoming_events 

import eventcalendar

class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm



    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            otp = forms.cleaned_data["otp"]
            print(otp)
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                action_description = f"{user} logged in."
                UserAction.objects.create(
                    user=request.user,  # User who performed the action
                    action=action_description,  # Description of the action
                )
                #phone_number = "9499469934"
                #print(phone_number)
                send_otp(request, otp)
                #return redirect("accounts:otp")
                #return redirect("dashboard")
                totp_device = TOTPDevice.objects.filter(user=user).first()
                if totp_device:
                    print("user has a totp device")
                    # If user has TOTP device, validate the OTP
                    if self.validate_otp(totp_device, otp):
                        # OTP is valid, proceed with login
                        return redirect("dashboard")
                    else:
                        # Invalid OTP, show error message
                        forms.add_error("otp", "Invalid OTP")
                        return render(request, self.template_name, {"form": forms})
                
                # If user doesn't have TOTP device, proceed with login without OTP validation
                return redirect("dashboard")
        
        # If form is invalid, render the form with errors
        context = {"form": forms}
        return render(request, self.template_name, context)

    def validate_otp(self, totp_device, otp):
        # Get the hex-encoded secret key from the TOTPDevice object
        secret_key_hex = totp_device.key
        # Decode the hex-encoded secret key into bytes
        secret_key_bytes = bytes.fromhex(secret_key_hex)
        # Convert the bytes secret key into a base32-encoded string
        secret_key_base32 = base64.b32encode(secret_key_bytes).decode('utf-8')
        # Create a TOTP object using the secret key
        totp = pyotp.TOTP(secret_key_base32)
        # Verify the OTP
        return totp.verify(otp)



    

class OTPView(View):
    template_name = 'accounts/otp.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        error_message = None
        otp = request.POST.get('otp')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    # WRITE CODE TO LOGIN USER HERE
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('dashboard')
                
                else:
                    pass
            else:
                pass
        else:
            pass

        # If OTP verification fails, render the template with error message
        return render(request, self.template_name, {'error_message': 'Invalid OTP'})



""" def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            otp = forms.cleaned_data["otp"]
            user = authenticate(request, username=email, password=password)
            
            if user:
                login(request, user)
                print("user has logged in but not fully")
                action_description = f"{user} logged in."
                UserAction.objects.create(
                    user=request.user,
                    action=action_description,
                )
                # Check if the user has a TOTP device
                totp_device = TOTPDevice.objects.filter(user=user).first()
                if totp_device:
                    print("user has a totp device")
                    # If user has TOTP device, validate the OTP
                    if self.validate_otp(totp_device, otp):
                        # OTP is valid, proceed with login
                        return redirect("dashboard")
                    else:
                        # Invalid OTP, show error message
                        forms.add_error("otp", "Invalid OTP")
                        return render(request, self.template_name, {"form": forms})
                
                # If user doesn't have TOTP device, proceed with login without OTP validation
                return redirect("dashboard")
        
        # If form is invalid, render the form with errors
        context = {"form": forms}
        return render(request, self.template_name, context)
    
    def validate_otp(self, totp_device, otp):
        totp = pyotp.TOTP(totp_device.config.seed)
        return totp.verify(otp)
    """