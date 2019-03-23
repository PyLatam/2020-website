import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from account import views
from account import forms as account_forms
from account.compat import is_authenticated

from . import forms


@never_cache
@login_required
def dashboard(request):
    context = {'reservations_url': settings.HOTEL_RESERVATIONS_URL}
    return render(request, 'account/dashboard.html', context)


@require_POST
@login_required
def register(request):
    form = forms.RegistrationForm(request.POST or None, user=request.user)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'errors': []})
    return JsonResponse({'success': False, 'errors': form.errors.get_json_data()})


class LoginView(views.LoginView):
    form_class = account_forms.LoginEmailForm


class LogoutView(views.LogoutView):

    def get(self, *args, **kwargs):
        if is_authenticated(self.request.user):
            auth.logout(self.request)
        return redirect(self.get_redirect_url())


class SignupView(views.SignupView):
    form_class = forms.SignupForm
    identifier_field = 'email'

    def generate_username(self, form):
        return str(uuid.uuid4())


class SettingsView(views.SettingsView):
    form_class = forms.SettingsForm

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def update_settings(self, form):
        self.update_user(form)

    def update_user(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save(update_fields=('first_name', 'last_name'))
