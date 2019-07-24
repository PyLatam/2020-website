from django import template

from sponsors.models import Sponsor


register = template.Library()


@register.simple_tag(takes_context=False)
def get_sponsors():
    sponsors = Sponsor.objects.filter(is_active=True)
    return sponsors.select_related('logo')
