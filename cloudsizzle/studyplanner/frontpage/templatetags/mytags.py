from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def startswith(val1, val2):
    return val1.startswith(val2)

