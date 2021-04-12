from django import template

register=template.Library()

@register.filter(name='multiply')
def multiply(number,number1):
    return number*number1

@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)