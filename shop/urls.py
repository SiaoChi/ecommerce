from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.shop , name = 'shop'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/', views.checkout , name ='checkout'),
    path('finish/',views.finish, name = 'finish'),

    path('update_item/',views.updateItem,name='update-item'),

]

