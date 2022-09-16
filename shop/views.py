import json

from django.shortcuts import render, redirect
from .models import *
from .form import *
from .until import cookieCart
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def shop(request):
    data = cookieCart(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    board = Board.objects.all()
    return render(request,'shop.html',locals())

def cart(request):
    cartdata = cookieCart(request)
    cartItems = cartdata['cartItems']
    order = cartdata['order']
    items = cartdata['items']

    if request.method == 'POST':
        if cartItems > 0:
            return redirect('checkout')

        else:
            messages.success(request, '購物車中沒有任何項目')
            pass
            print('pass')


    return render(request,'cart.html',locals())

def checkout(request):
    board = Board.objects.all()
    form = OrderForm()
    cartdata = cookieCart(request)

    cartItems = cartdata['cartItems']
    order = cartdata['order']
    items = cartdata['items']

    if request.method == "POST":
        # 查一下request.post是什麼
        form = OrderForm(request.POST)
        # print('test')
        # print(form)
        if form.is_valid():
            form.save()
            cartItems = 0
            order['get_cart_total'] = 0
            order['get_cart_items'] = 0
            order['get_save_money'] = 0
            items = []
            form = OrderForm()
        messages.success(request, '你的訂單完成，已同步寄信到您的信箱，請留意匯款時間。')
        return redirect('finish')

    return render(request,'checkout.html',locals())

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print("ProductId", productId)

    product = Product.objects.get(id=productId)
    order = Order.objects.get_or_create(complete =False)
    orderItem = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def finish(request):
    board = Board.objects.all()
    cartdata = cookieCart(request)

    cartItems = cartdata['cartItems']
    order = cartdata['order']
    items = cartdata['items']

    return render(request, 'finish.html', locals())
