from django.urls import path
from accounts.views.signup import SignUpView
from accounts.views.signin import SignInView
from accounts.views.signout import signout
from accounts.views.signin import OTPView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", signout, name="signout"),
    path("otp/", OTPView.as_view(), name='otp'),
]
