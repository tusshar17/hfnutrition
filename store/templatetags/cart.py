from django import template

register = template.Library()


@register.filter(name= "cart_quantity")
def cart_quantity(product, cart):
    return cart.get(str(product.id))


@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[str(k)]


# calculating order summary if user not logged in
def price_total(product, cart):
    return product.selling_price * cart_quantity(product, cart)

@register.filter(name="total_cart_price")
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p, cart)

    return sum


def mrp_total(product, cart):
    return product.mrp * cart_quantity(product, cart)

@register.filter(name="total_cart_mrp")
def total_cart_mrp(products, cart):
    sum = 0
    for p in products:
        sum += mrp_total(p, cart)

    return sum

@register.filter(name="total_discount")
def total_discount(products, cart):
    t_mrp = total_cart_mrp(products, cart)
    t_price = total_cart_price(products, cart)
    return t_mrp-t_price



# calculating order summary if user logged in
@register.filter(name="total_cart_price_1")
def total_cart_price_1(cart):
    sum = 0
    for p in cart:
        sum += p.product.selling_price * p.qty

    return sum

@register.filter(name="total_cart_mrp_1")
def total_cart_mrp_1(cart):
    sum = 0
    for p in cart:
        sum += p.product.mrp * p.qty

    return sum

@register.filter(name="total_discount_1")
def total_discount_1(cart):
    t_mrp = total_cart_mrp_1(cart)
    t_price = total_cart_price_1(cart)
    return t_mrp-t_price


