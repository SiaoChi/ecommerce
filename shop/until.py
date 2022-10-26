import json
from .models import *
from .form import *
from django.http import JsonResponse

import os
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages

# def Coupon(request):
#
#         now = timezone.now()
#         coupon_form = CouponForm(request.POST)
#         if coupon_form.is_valid():
#             code = coupon_form.cleaned_data['code']
#             try:
#                 couponObj = Coupon.objects.get(code__iexact= code,
#                                             valid_from__lte=now,
#                                             valid_to__gte=now,
#                                             active=True)
#             except:
#                 messages.alert(request, '優惠碼無效')
#
#     context = {'couponObj':couponObj }
#
#     return context

def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'get_save_money':0}
    cartItems = order['get_cart_items']  # 0

    # cart = {book:{quantuty:1} ,pen:{quantity:2}
    # {'get_cart_items':1}

    #把在cookie裏的資料解析
    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if (cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']  # 1

                product = Product.objects.get(id=i)
                total = (product.promotion * cart[i]['quantity'])


                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                order['get_save_money'] += (product.price * cart[i]['quantity'])-(product.promotion * cart[i]['quantity'])

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.image.url, 'promotion':product.promotion, } ,
                    'quantity': cart[i]['quantity'],'get_total':total,
                }
                items.append(item)

        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def update_cookie(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'get_save_money':0}
    cartItems = order['get_cart_items']  # 0

    # cart = {book:{quantuty:1} ,pen:{quantity:2}
    # {'get_cart_items':1}

    #把在cookie裏的資料解析
    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if (cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']  # 1

                product = Product.objects.get(id=i)
                total = (product.promotion * cart[i]['quantity'])


                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                order['get_save_money'] += (product.price * cart[i]['quantity'])-(product.promotion * cart[i]['quantity'])

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.image.url, 'promotion':product.promotion, } ,
                    'quantity': cart[i]['quantity'],'get_total':total,
                }
                items.append(item)


        except:
            pass

    order_json = json.dumps(order)



    return JsonResponse(order_json, safe=False)


