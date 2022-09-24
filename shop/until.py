import json
from .models import *
import os
from django.core.files.storage import default_storage
from django.db.models import FileField


# add cart item
# if (action == 'add'){
# 		if (cart[productId] == undefined){
# 		cart[productId] = {'quantity':1}
#
# 		}else{
# 			cart[productId]['quantity'] += 1
# 		}

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


