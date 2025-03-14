from django import template

register = template.Library()

@register.simple_tag
def get_obj(obj, val, val2=False):
    if val2:
        return obj[val][val2]
    else:
        return obj[val]
