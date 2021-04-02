import json
from .models import *

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_quantity': 0, 'shipping': False}
    cartItems = order['get_cart_quantity']

    for i in cart:
        try:
            quantity = cart[i]['quantity']
            cartItems += quantity
            product = Product.objects.get(id=i)
            total = (product.price * quantity)
            
            order['get_cart_total'] += total
            order['get_cart_quantity'] += quantity

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': quantity,
                'get_total': total
            }

            items.append(item)
            if not product.digital:
                order['shipping'] = True
        except:
            pass
    
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
        }