import uuid

from account import views
from account import forms as account_forms

from . import forms


class SignupView(views.SignupView):
    form_class = forms.SignupForm
    identifier_field = 'email'

    def generate_username(self, form):
        return str(uuid.uuid4())


class LoginView(views.LoginView):
    form_class = account_forms.LoginEmailForm
