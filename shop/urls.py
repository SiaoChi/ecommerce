from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.shop , name = 'shop'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/', views.checkout , name ='checkout'),
    path('summernote/', include('django_summernote.urls')),
    #參考網址 https://blog.twshop.asia/django-%E6%89%80%E8%A6%8B%E5%8D%B3%E6%89%80%E5%BE%97-%E5%AF%8C%E6%96%87%E6%9C%AC%E7%B7%A8%E8%BC%AF%E5%99%A8-ckeditor/
    # path('finish/',views.finish, name = 'finish'),

    # path('update_item/',views.updateItem,name='update-item'),

]

