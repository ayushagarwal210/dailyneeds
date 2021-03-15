from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(item,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==item.id:
            return True      
    # print(keys)
    # print(item,cart)
    return False

@register.filter(name='cart_quantity')
def is_in_cart(item,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==item.id:
            return cart.get(id)      
    # print(keys)
    # print(item,cart)
    return 0