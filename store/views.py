from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_quantity': 0}
    context = {
        "order": order,
        "items": items
        }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # will get all order items with the order parent
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_quantity': 0}
    context = {
        "order": order,
        "items": items
        }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action', action)
    print('Product', productId)
    return JsonResponse('Item was added', safe=False)