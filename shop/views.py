import json
from django.shortcuts import render, redirect
from .models import *
from .form import *
from .until import cookieCart , Coupon
from django.http import JsonResponse
from django.contrib import messages

#mail的套組
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone



# Create your views here.

def shop(request):
    request.session.flush()
    cartdata = cookieCart(request)
    carousel = Carousel.objects.all()
    cartItems = cartdata['cartItems']
    order = cartdata['order']
    order_total = order['get_cart_total']

    products = Product.objects.all()
    board = Board.objects.all()
    print(request.session.items())
    return render(request, 'index.html', locals())

def cart(request):
    # request.session.flush()
    cartdata = cookieCart(request)
    cartItems = cartdata['cartItems']
    order = cartdata['order']
    items = cartdata['items']
    order_total = order['get_cart_total']
    coupon_form = CouponForm()
    delivery_f = DeliverForm()

    # 運費
    if order_total >= 1000:
        shipping_fee = 0
        shipping_total = order_total
        selected_deliver = request.session.get('delivery')
        print('1 費用小於一千，免運費')
    elif request.session.get('shipping_fee'):
        shipping_fee = request.session['shipping_fee']
        print('2 費用小於一千運費',shipping_fee)
        selected_deliver = request.session.get('delivery')
        shipping_total = order_total + shipping_fee
    else:
        shipping_fee = 0
        selected_deliver = ''
        shipping_total = order_total
        print('3 費用小於一千運費')

    request.session['shipping_total']= shipping_total
    request.session['shipping_fee'] = shipping_fee

    # 優惠碼送出
    if request.method == "POST" and 'coupon' in request.POST:
        now = timezone.now()
        # print(now)
        coupon_form = CouponForm(request.POST)
        # print(coupon_form)
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data['code']

            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)

                after_discount_total = int(order_total) + shipping_fee - int(coupon.discount)

                if after_discount_total <= 0:
                    messages.success(request, '無法使用折扣，折扣後金額不得小於或等於0')
                    after_discount_total = 0
                else:
                    pass
                    messages.success(request, '優惠碼有效')

                request.session['coupon_used'] = True
                request.session['after_discount_total'] = after_discount_total
                request.session['coupon.discount'] = coupon.discount

            # print except的問題
            except Exception as e:
                print(e)
                if str(e) == 'Coupon matching query does not exist.':
                    messages.warning(request, '優惠碼無效')
                else:
                    messages.warning(request, '未知的錯誤')


    # 結帳按鈕
    if request.method == 'POST' and 'checkout' in request.POST:
        if request.session.get('delivery') and cartItems > 0:
            return redirect('checkout')

        elif  cartItems <= 0:
            messages.success(request, '購物車中沒有任何項目')
            pass
            print('pass')

        else:
            messages.success(request, '請選擇運送方式')
            print(request.session.items())
            pass

    request.session.get_expire_at_browser_close()
    return render(request,'cart.html',locals())



def checkout(request):
    # 畫面資訊
    try:
        check_board = Board.objects.all()
        cartdata = cookieCart(request)
        form = OrderForm()
        cartItems = cartdata['cartItems']
        order = cartdata['order']
        shipping_fee = request.session['shipping_fee']
        order_total = order['get_cart_total']
        items = cartdata['items']
        checkout_board = Board.objects.get(id = 1).checkout_board

        shipping_total = request.session['shipping_total']
        selected_deliver = request.session.get('delivery')

        print(request.session.items())

        if request.session.get('after_discount_total'):
            after_discount_total = request.session['after_discount_total']
            coupon_discount = request.session['coupon.discount']
        else:
            coupon_discount = 0

        #訂購資訊表單送出
        if request.method == "POST" and 'order' in request.POST:
            form = OrderForm(request.POST)
            if form.is_valid():
                form = form.save(commit = False)
                form.delivery_price = shipping_fee
                form.coupon_price = coupon_discount
                form.total_price = shipping_total
                form.delivery_company = str(request.session['delivery'])
                # print('儲存form')
                # print(form.delivery_price,form.coupon_price,form.total_price,form.delivery_company)
                form.save()
                # print(form.instance.id)
                shop_items = ''
                #以下把cookCart中的訂購的item拆解成訂單可以存檔案資料
                for item in items:
                    productId = item['id']
                    formId = form.id  #如果上方沒有把form變成var 這邊就會是form.instance.id
                    product = Product.objects.get(id=productId)
                    created_order = Order.objects.get(id = formId)
                    orderItem = OrderItem.objects.create(order=created_order, product=product,quantity=item['quantity'])
                    orderItem.save()
                    #代表這個訂單填寫的mail
                    order_mail = created_order.mail
                    #代表每個購物項目的資訊，會forloop後，包進mail messages裏面
                    shop_items +=  "{}：{}元，{}個\n".format(item['product']['name'], item['product']['promotion'], item['quantity'])
                    delivery_store = created_order.delivery_store
                    id_to_customer = str(formId)[0:8]
                    print(id_to_customer)


                    # 以下為自動寄信功能
                    # 使用優惠碼，mail費用有差別

                    if request.session.get('coupon_used'):
                        email_messages = shop_items + "\n您的運送方式：{}\n店到店門市：{}\n運費：{}元\n使用折扣碼折抵{}元\n折扣後總金額{}元\n感謝您的訂購！\n\n 【匯款帳戶資訊】\n匯款銀行帳戶： 中國信託 822\n戶 名： 莊筱詩\n帳 號：576-540-236-363\n提醒您：請於三日內匯款訂單才會正式成立唷！♥".format(
                            selected_deliver,delivery_store,shipping_fee, coupon_discount, after_discount_total)
                    else:
                        email_messages = shop_items + "\n您的運送方式：{}\n店到店門市：{}\n運費：{}元\n以上共計{}元\n感謝您的訂購！\n\n 【匯款帳戶資訊】\n匯款銀行帳戶： 中國信託 822\n戶 名： 莊筱詩\n帳 號：576-540-236-363\n提醒您：請於三日內匯款訂單才會正式成立唷！♥".format(
                            selected_deliver,delivery_store,shipping_fee, shipping_total )

                email_template = render_to_string('email.html',
                                                  {'username': created_order.name,
                                                   'email_messages': email_messages,
                                                   'address': created_order.address,
                                                   'phone': created_order.phone,
                                                   'orderID':id_to_customer,
                                                   'orderDate':created_order.datetime,
                                                   # 'checkout_board':checkout_board,
                                                   }
                                                  )

                email = EmailMessage(
                    '【嘻嘻選物】通知信：感謝你的訂購',  # 電子郵件標題
                    email_template,  # 郵件內容
                    settings.EMAIL_HOST_USER,  # 寄件人
                    [order_mail]  # 收件者
                )

                email.fail_silently = False
                email.send()

                messages.success(request, '你的訂單完成，已同步寄信到您的信箱，請留意匯款時間。')

            form = OrderForm()
            cartdata.clear()
            order.clear()
            items.clear()
            cartItems = 0

            print(request.session.items())

            #刪除session的資料，避免重複購買資料有誤
            # for key in list(request.session.keys()):
            #     del request.session[key]
            request.session.flush()

            # return render(request,'checkout.html',locals())


        return render(request,'checkout.html',locals())

    except:
        # pass
        return render(request, 'checkout.html')


def updateDeliver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data_json = json.dumps(data)
            delivery_company = data['delivery']
            delivery_obj = DeliverCompany.objects.get(company=delivery_company)
            # request.session['deliver_id'] = delivery_obj.id
            request.session['delivery'] = delivery_obj.company
            print('4',delivery_obj.company)
            # delivery_selected = delivery_obj.company
            shipping_fee = delivery_obj.fee
            request.session['shipping_fee']=shipping_fee
            print(delivery_obj)
            print(request.session['shipping_fee'])
        except:
            messages.warning(request,'未知錯誤')

    context = {'shipping_fee': shipping_fee, 'data':data }
    # print(data_json)
    # print(type(data_json))

    return JsonResponse(data_json, safe=False)
    # return cart(request)

def update_order(request):
    request.session.flush()
    return redirect('/cart')

def payment_report(request):
    form = PaymentReportForm()
    if request.method == "POST":

        try:
            form = PaymentReportForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '收到您的匯款回報，我們會盡快審查，欲查詢進度請點擊「訂單進度查詢」，感謝！')
                form = PaymentReportForm()
        except:
            messages.warning(request,'請檢查表單或直接聯絡團購人員')

    context = {'form':form,'messages':messages}

    return render(request,'payment-report.html',locals())

def order_report(request):
    form = OrderReportForm()
    if request.method == "POST":
        try:
            form = OrderReportForm(request.POST)
            if form.is_valid():
                orderId = form.cleaned_data['orderId']
                orderPhone = form.cleaned_data['phone']
                print('1')
                orderObj = Order.objects.get(id__icontains =orderId)
                orderPhone == orderObj.phone
                print(orderObj)
                orderId = orderObj.id
                print(orderId)
                print(orderObj.transfer)
                return redirect('order-process', orderId)

        except:
            messages.warning(request,'資訊錯誤，請再次確認您的表單資訊。')

    return render(request, 'order-report.html', locals())

def order_process(request,pk):
    order = Order.objects.get(id=pk)
    id_to_customer = str(order.id)[0:8]

    context = {'order':order,'id_to_customer':id_to_customer}

    return render(request, 'order-process.html',context)