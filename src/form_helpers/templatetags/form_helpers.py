from django import template

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
