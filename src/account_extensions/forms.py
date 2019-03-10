from django import forms
from django.utils.translation import ugettext_lazy as _

import account.forms


class SignupForm(account.forms.SignupForm):
    username = None
    # first_name = forms.CharField(max_length=250, label=_('first name'))
    # last_name = forms.CharField(max_length=250, label=_('last name'))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput()


class SettingsForm(forms.Form):
    first_name = forms.CharField(max_length=250, label=_('first name'))
    last_name = forms.CharField(max_length=250, label=_('last name'))
