import json

from django.shortcuts import render, redirect
from .models import *
from .form import *
from .until import cookieCart
from django.http import JsonResponse
from django.contrib import messages

#mail的套組
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string





# Create your views here.

def shop(request):
    data = cookieCart(request)
    homeImgs = Carousel.objects.all()

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
    check_board = Board.objects.all()
    cartdata = cookieCart(request)
    form = OrderForm()
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
            # print(form.instance.id)
            shop_item = ''
            for item in items:
                # print(items[0])
                productId = item['id']
                formId = form.instance.id
                product = Product.objects.get(id=productId)
                _order = Order.objects.get(id = formId)
                orderItem = OrderItem.objects.create(order=_order, product=product,quantity=item['quantity'])
                orderItem.save()
                order_mail = _order.mail
                shop_item +=  "{}：{}元，{}個\n".format(item['product']['name'], item['product']['promotion'], item['quantity'])

        form = OrderForm()

        email_messages = shop_item + "\n以上共計{}元\n感謝您的訂購！\n\n 【匯款帳戶資訊】\n匯款銀行帳戶： 中國信託 822\n戶 名： 莊筱詩\n帳 號：576-540-236-363\n提醒您：請於三日內匯款訂單才會正式成立唷！♥".format(order['get_cart_total'])


        email_template = render_to_string('email.html',
                                          {'username':_order.name,
                                           'email_messages':email_messages,
                                           'address':_order.address,
                                           'phone':_order.phone,}
                                          )

        email = EmailMessage(
            '通知信：感謝你的訂購', #電子郵件標題
            email_template, #郵件內容
            settings.EMAIL_HOST_USER, #寄件人
            [order_mail] #收件者
        )

        email.fail_silently = False
        email.send()

        messages.success(request, '你的訂單完成，已同步寄信到您的信箱，請留意匯款時間。')
        cartdata.clear()
        order.clear()
        items.clear()
        cartItems = 0
        print(cartdata)
        return render(request,'checkout.html',locals())

    return render(request,'checkout.html',locals())

# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action:',action)
#     print("ProductId", productId)
#
#     product = Product.objects.get(id=productId)
#     order = Order.objects.get_or_create(complete =False)
#     orderItem = OrderItem.objects.get_or_create(order=order, product=product)
#
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity +1)
#         print('add item')
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity -1)
#         print('decrease item')
#
#     elif action == 'delete':
#         orderItem.delete()
#
#     # orderItem.save()
#     # print('item save')
#
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#
#     return JsonResponse('Item was added',safe=False)

#沒使用到
# def finish(request):
#     board = Board.objects.all()
#
#
#     return render(request, 'finish.html', locals())
