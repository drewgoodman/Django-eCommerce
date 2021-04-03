from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cartData, cookieCart, guestOrder

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        "order": order,
        "items": items,
        "cartItems": cartItems
        }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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

    else:
        print("User not logged in")
        print('COOKIES:', request.COOKIES)
        customer, order = guestOrder(request, data)

    total = float(data['userFormData']['total'])
    order.transaction_id = transaction_id

    print("Total",total)
    print('Cart Total:',order.get_cart_total)
    if total == float(order.get_cart_total): # check backend data against front end data being passed for integrity
        print("Complete!")
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


    return JsonResponse('Payment Complete', safe=False)