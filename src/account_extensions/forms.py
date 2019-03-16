from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

import account.forms

from core.models import ConferenceRegistration, Reservation
from core.helpers import get_reservation


class RegistrationForm(forms.Form):
    email = forms.EmailField(label=_('reservation email'))
    reservation_number = forms.IntegerField(label=_('reservation #'), min_value=1)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.reservation = None
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        if self.errors:
            return data

        if ConferenceRegistration.exists_for_user(self.user):
            msg = ugettext('You\'ve already registered')
            raise forms.ValidationError(msg)

        reservation = get_reservation(
            email=data['email'],
            number=data['reservation_number'],
        )

        if not reservation:
            msg = ugettext('Unable to find matching reservation')
            raise forms.ValidationError(msg)

        if not reservation.status == 'Reserved':
            msg = ugettext('The reservation is not active')
            raise forms.ValidationError(msg)

        try:
            self.reservation = Reservation.objects.get(number=data['reservation_number'])
        except Reservation.DoesNotExist:
            self.reservation = Reservation(number=data['reservation_number'])
        self.reservation.name = reservation.name
        self.reservation.email = reservation.email
        self.reservation.occupancy = reservation.occupancy
        self.reservation.checkin = reservation.checkin
        self.reservation.checkout = reservation.checkout
        self.reservation.save()

        if not self.reservation.has_vacancies():
            msg = ugettext('The reservation is fully booked '
                           'and no longer has vacancies.')
            raise forms.ValidationError(msg)
        return data

    def save(self):
        registration = ConferenceRegistration.objects.create(
            account=self.user.account,
            reservation=self.reservation,
        )
        return registration


class SignupForm(account.forms.SignupForm):
    username = None
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput()


class SettingsForm(account.forms.SettingsForm):
    email = None
    timezone = None
    language = None
    first_name = forms.CharField(max_length=250, label=_('first name'))
    last_name = forms.CharField(max_length=250, label=_('last name'))
