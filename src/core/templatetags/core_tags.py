from datetime import date, datetime

from django import template
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import override

from .. import constants
from ..models import ConferenceRegistration


register = template.Library()


@register.simple_tag(takes_context=True)
def get_current_url(context, language):
    match = context['request'].resolver_match
    args = match.args or None
    kwargs = match.kwargs or None

    with override(language):
        return reverse(match.url_name, args=args, kwargs=kwargs)


@register.simple_tag()
def get_days_left():
    start_date = datetime(year=2019, month=8, day=29)
    return (timezone.make_aware(start_date) - timezone.now()).days


@register.simple_tag()
def render_widget(field, placeholder='', input_classes=''):
    attrs = {'placeholder': placeholder or field.label}

    if input_classes:
        attrs['classes'] = input_classes
    return mark_safe(field.as_widget(attrs=attrs))


@register.simple_tag()
def get_conference_dates():
    checkin_dates = (
        ('20190828', date(year=2019, month=8, day=28)),
        ('20190829', date(year=2019, month=8, day=29)),
        ('20190830', date(year=2019, month=8, day=30)),
    )
    checkout_dates = (
        ('20190901', date(year=2019, month=9, day=1)),
        ('20190902', date(year=2019, month=9, day=2)),
        ('20190903', date(year=2019, month=9, day=3)),
    )
    return {'checkin': checkin_dates, 'checkout': checkout_dates}


@register.simple_tag(takes_context=True)
def get_conference_registration(context):
    user = context['request'].user

    if user.is_authenticated:
        registration = ConferenceRegistration.get_for_user(user)
    else:
        registration = None

    if not registration:
        registration = {
            'ready': False,
            'missing': [
                constants.RESERVATION_REQUIRED,
                constants.FULL_NAME_REQUIRED,
            ],
        }
    return registration
