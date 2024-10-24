import pyotp
from datetime import datetime, timedelta

def send_otp(request, phone_number):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)

    print(f"Your one time password is {otp} and it was sent to {phone_number}")
    # USE TWILIO CODE TO SEND IT TO THE PHONE NUMBER
