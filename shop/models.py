from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=40, verbose_name='產品名')
    price = models.IntegerField(verbose_name ='原價')
    promotion = models.IntegerField(verbose_name ='特價')
    detail = models.TextField(max_length= 500 , verbose_name= '商品說明')
    image = models.ImageField(null=True, blank=True , verbose_name= '圖片',upload_to="product")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class ProductImage(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image = models.FileField(upload_to='images')

    def __str__(self):
        return self.product.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    name = models.CharField(max_length=10,verbose_name='收件人', null=False)
    phone = models.CharField(max_length=12,verbose_name='手機號碼', null=False)
    mail = models.EmailField(null= True, verbose_name='電子信箱')
    zipcode = models.CharField(max_length=6, null=False,verbose_name='郵遞區號')
    address = models.CharField(max_length=200, null=False,verbose_name='地址')
    complete = models.BooleanField(default=False)
    message = models.CharField(max_length=200,null=True,verbose_name='備註欄')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    #得到訂單總金額
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

    #得到訂單數量
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    #取得訂單內容
    @property
    def get_cart_all(self):
        orderproducts = self.orderitem_set.all()
        return orderproducts

#為了計算單項item的費用，才能讓order知道總價，讓前端的數量可以修改
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Board(models.Model):
    home_board = models.TextField(max_length=500, verbose_name='首頁公布欄')
    checkout_board = models.TextField(max_length=500, verbose_name='結帳公布欄')




