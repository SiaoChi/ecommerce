from django.contrib import admin
from django.urls import path
from . import views
from . import until
from django.urls import include


urlpatterns = [
    #網頁path
    path('', views.shop, name ='index'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/', views.checkout , name ='checkout'),
    path('summernote/', include('django_summernote.urls')),
    path('payment-report/',views.payment_report, name='payment-report'),
    path('order-report/',views.order_report, name='order-report'),
    path('order-process/<str:pk>',views.order_process,name='order-process'),


    # 功能path
    path('cart/update_deliver/',views.updateDeliver,name='update-deliver'),
    path('cart/update_order/',views.update_order,name='update-order'),
    path('update_cookie/',until.update_cookie,name='update-cookie'),
    # path('update_item/',views.updateItem,name='update-item'),

]

#參考網址 https://blog.twshop.asia/django-%E6%89%80%E8%A6%8B%E5%8D%B3%E6%89%80%E5%BE%97-%E5%AF%8C%E6%96%87%E6%9C%AC%E7%B7%A8%E8%BC%AF%E5%99%A8-ckeditor/
