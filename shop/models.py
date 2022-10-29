from django.db import models
import uuid
import django.utils.timezone as timezone
from django.utils.translation import gettext_lazy as _

#壓縮圖檔module
from io import BytesIO
from PIL import Image
from django.core.files import File

# Create your models here.

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'WebP', quality=80, optimize =True)
    new_image = File(im_io, name=image.name)
    return new_image

class Product(models.Model):
    name = models.CharField(max_length=40, verbose_name='產品名')
    price = models.IntegerField(verbose_name ='原價')
    promotion = models.IntegerField(verbose_name ='特價')
    detail = models.TextField(max_length= 700 , verbose_name= '商品說明')
    image = models.ImageField(null=True, blank=True , verbose_name= '圖片',upload_to="product")

    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
        print('compressed!')


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

CHOICES_BOOLEANO_YESNO = (
    (True, _('是')),
    (False, _('否'))
)

CHOICES_FOR_ORDER = {
    ('是','是'),
    ('否','否'),
}

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, verbose_name='訂單編號')
    name = models.CharField(max_length=10,verbose_name='收件人', null=False)
    phone = models.CharField(max_length=12,verbose_name='手機號碼', null=False)
    mail = models.EmailField(null= True, verbose_name='電子信箱')
    zipcode = models.CharField(max_length=6, null=True, blank= True,verbose_name='郵遞區號')
    address = models.CharField(max_length=200, null=True, blank= True,verbose_name='地址')
    delivery_company = models.CharField(max_length=20, null=True,blank= True,verbose_name='運送超市')
    delivery_store = models.CharField(max_length=20, null=True,blank= True,verbose_name='店到店門市' )
    message = models.TextField(max_length=500,null=True, blank= True ,verbose_name='備註欄')
    datetime = models.DateTimeField(auto_now_add=True)
    delivery_price = models.IntegerField(verbose_name='運費',default=0, null=True,blank=True)
    coupon_price = models.IntegerField(verbose_name='優惠卷折扣',default=0, null=True,blank=True)
    total_price = models.IntegerField(verbose_name='結帳金額',default=0, null=True,blank=True)
    transfer = models.CharField(max_length=20, default='否', verbose_name='收到款項', choices =CHOICES_FOR_ORDER)
    complete = models.CharField(max_length=20, default='否',verbose_name='已寄出訂單', choices =CHOICES_FOR_ORDER)


    # help_text = "請輸入有效的電子信箱"

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
    #ForeignKey是外子，父層是後面填寫的Model，
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


    def __str__(self):
        return self.product.name

class Board(models.Model):
    home_board = models.TextField(max_length=500, verbose_name='首頁公布欄')
    checkout_board = models.TextField(max_length=500, verbose_name='結帳公布欄')

    def __str__(self):
        return '佈告欄'

class Carousel(models.Model):
    title = models.CharField(max_length=30, verbose_name='主標',null=True, blank=True)
    description = models.TextField(max_length=200, verbose_name='描述',null=True, blank=True)
    image = models.ImageField(null=True, blank=True , verbose_name= '圖片',upload_to="carousel")

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Coupon(models.Model):
    name = models.CharField(max_length=20, verbose_name='優惠券名稱')
    code = models.CharField(max_length=10, verbose_name='優惠碼')
    discount = models.IntegerField(verbose_name='折扣費用')
    valid_from = models.DateTimeField( verbose_name='開始日期')
    valid_to = models.DateTimeField( verbose_name='結束日期')
    active = models.BooleanField (verbose_name ='啟用')

    def __str__(self):
        return self.name


class Delivery(models.Model):
    delivery = models.ManyToManyField('DeliverCompany', verbose_name ='選擇送貨方式')

    def __str__(self):
        return self.delivery

class DeliverCompany(models.Model):
    company = models.CharField(max_length=10, verbose_name= '運送方式')
    fee = models.IntegerField(verbose_name ='運費')

    def __str__(self):
        return self.company

class PaymentReport(models.Model):
    transfername = models.CharField(max_length=10,verbose_name= '匯款人姓名',null=False, blank=False)
    transferNums = models.CharField(max_length=15 ,verbose_name ="帳號後五碼",null=False, blank=False)
    transferPrice = models.CharField(max_length=15 ,verbose_name ="匯款金額",null=False, blank=False)
    transferdate = models.CharField(max_length=15 ,verbose_name ="匯款日期",null=False, blank=False)
    sendingdate = models.DateTimeField(default = timezone.now, verbose_name ="填表單日期")

    def __str__(self):
        return self.transfername