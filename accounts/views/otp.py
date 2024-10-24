from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth import authenticate, login

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    #WRITE CODE TO LOGIN USER

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('main')

    return render(request, 'accounts/otp.html', {})