from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('form_helpers/field.html')
def render_field(field, placeholder='', help_text=''):
    context = {
        'field': field,
        'widget': field.field.widget,
        'help_text': help_text or field.help_text,
        'placeholder': placeholder or field.label,
    }
    return context


@register.simple_tag()
def render_widget(field, placeholder='', input_classes=''):
    attrs = {'placeholder': placeholder or field.label}

    if input_classes:
        attrs['classes'] = input_classes
    return mark_safe(field.as_widget(attrs=attrs))
