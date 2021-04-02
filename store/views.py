from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookie_cart

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
        cartItems = order.get_cart_quantity
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
        cartItems = order.get_cart_quantity
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        "order": order,
        "items": items,
        "cartItems": cartItems
        }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
        cartItems = order.get_cart_quantity
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context = {
        "order": order,
        "items": items,
        "cartItems": cartItems
        }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action', action)
    print('Product', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['userFormData']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total: # check backend data against front end data being passed for integrity
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                state=data['shippingInfo']['state'],
                zipcode=data['shippingInfo']['zipcode']
            )
    else:
        print("User not logged in")
    return JsonResponse('Payment Complete', safe=False)