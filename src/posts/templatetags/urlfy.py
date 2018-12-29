from urllib.parse import quote
from django import template

register = template.Library()

# @register.filter means that we are registering it as filter
@register.filter
def urlify(value):
    return quote(value)
