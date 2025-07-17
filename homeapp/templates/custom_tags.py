# homeapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def in_list(value, arg):
    return value in arg.split(',')
