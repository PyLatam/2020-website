import uuid

from django.contrib import auth
from django.shortcuts import render, redirect

from account import views
from account import forms as account_forms
from account.compat import is_authenticated

from . import forms


def dashboard(request):
    return render(request, 'account/dashboard.html')


class SignupView(views.SignupView):
    form_class = forms.SignupForm
    identifier_field = 'email'

    def generate_username(self, form):
        return str(uuid.uuid4())


class LoginView(views.LoginView):
    form_class = account_forms.LoginEmailForm


class LogoutView(views.LogoutView):

    def get(self, *args, **kwargs):
        if is_authenticated(self.request.user):
            auth.logout(self.request)
        return redirect(self.get_redirect_url())
