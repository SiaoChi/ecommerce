from .models import *
from django.forms import ModelForm
from django import forms
from django_summernote.widgets import SummernoteWidget

# class Order_storetostore_Form(ModelForm):
#     class Meta:
#         model = Order
#         fields ="__all__"
#         exclude = ['datetime', 'complete']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': '收件人真實姓名'}),
#             'phone': forms.TextInput(attrs={'placeholder': '手機號碼'}),
#             'mail': forms.TextInput(attrs={'placeholder': 'ex@gmail.com'}),
#             'delivery': forms.TextInput(attrs={'placeholder': '店到店門市名稱'}),
#             'message': forms.TextInput(attrs={'placeholder': '訂單備註：例如運送時間'}),
#             # 'delivery': forms.Select(attrs={'class': 'select'}),
#
#         }
#         labels = {
#             'name':'收件人',
#             'phone':'手機號碼',
#             'mail':'電子信箱',
#             'delivery':'店到店門市',
#             'message':'訂單備註',
#
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ="__all__"
        exclude = ['delivery_company','delivery_price','transfer','total_price','coupon_price','datetime', 'complete']
        widgets = {
            # 'name': forms.TextInput(attrs={'placeholder': '真實姓名'}),
            # 'phone': forms.TextInput(attrs={'placeholder': '手機號碼'}),
            # 'mail': forms.TextInput(attrs={'placeholder': 'ex@gmail.com'}),
            # 'zipcode': forms.TextInput(attrs={'placeholder': 'ex.110'}),
            # 'address': forms.TextInput(attrs={'placeholder': '縣市市區、街道名稱與門牌號碼'}),
            # 'delivery_store':forms.TextInput(attrs={'placeholder': '宅配到府，請跳過'}),
            # 'message': forms.TextInput(attrs={'placeholder': '訂單備註：非必要'}),
            # 'delivery': forms.Select(attrs={'class': 'select'}),

        }
        labels = {
            'name':'真實姓名',
            'phone':'手機號碼',
            'mail':'電子信箱',
            'zipcode':'郵遞區號  (店到店，不須填寫）',
            'address':'地址 (店到店，不須填寫）',
            'delivery_store':'取貨門市(店到店填寫）',
            'message':'訂單備註',

        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': '請輸入優惠碼','class':'input'}),
        }
        labels = {
            'code':'優惠碼'
        }

class DeliverForm(ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"
        exclude = ['order']
        widgets = {
             'delivery': forms.Select(attrs={'class': 'select','onChange':'updateDeliver()'}),
        }
        label = {
            'delivery': '運送方式'
        }

    def __init__(self, *args, **kwargs):
        super(DeliverForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class PaymentReportForm(ModelForm):
    class Meta:
        model = PaymentReport
        fields = '__all__'
        exclude = ['sendingdate']

    def __init__(self, *args, **kwargs):
        super(PaymentReportForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


#不來自modelform的form
class OrderReportForm(forms.Form):

    orderId = forms.CharField(label='訂單編號',
                              max_length=8,min_length=8,
                              widget= forms.TextInput(attrs={'class':'input','placeholder':'請輸入訂單編號共八碼'},))

    phone = forms.CharField(label='手機號碼',max_length=10,min_length=10,
                            widget= forms.TextInput(attrs={'class':'input','placeholder':'請輸入手機號碼共十碼'},))


# https://github.com/summernote/django-summernote 新增summernote會使用到