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
def cart_quantity(item,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==item.id:
            return cart.get(id)      
    # print(keys)
    # print(item,cart)
    return 0

@register.filter(name='price_total')
def price_total(item,cart):
    return item.price*cart_quantity(item,cart)

@register.filter(name='total_cart_price')
def total_cart_price(items,cart):
    sum=0
    for i in items:
        sum+=price_total(i,cart)
    return sum