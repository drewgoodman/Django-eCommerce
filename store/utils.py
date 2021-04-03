import json
from .models import *

def cookieCart(request):
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

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
        cartItems = order.get_cart_quantity
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
        }

def guestOrder(request, data):
    name = data['userFormData']['name']
    email = data['userFormData']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order