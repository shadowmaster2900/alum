from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice

from accounts.forms import SignUpForm


class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            user = forms.save()
            TOTPDevice.objects.create(user=user, name=user.email, confirmed=True, tolerance=90)
            return redirect("accounts:signin")
        context = {"form": forms}
        return render(request, self.template_name, context)
