from .models import *
from django.forms import ModelForm
from django import forms
from django_summernote.widgets import SummernoteWidget

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ="__all__"
        exclude = ['datetime', 'complete']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '陳小美'}),
            'phone': forms.TextInput(attrs={'placeholder': '0900-123-123'}),
            'mail': forms.TextInput(attrs={'placeholder': 'ex@gmail.com'}),
            'zipcode': forms.TextInput(attrs={'placeholder': '110'}),
            'address': forms.TextInput(attrs={'placeholder': '台北市大安區...'}),
            'message': forms.TextInput(attrs={'placeholder': '非必要項目'}),

        }
        labels = {
            'name':'收件姓名',
            'phone':'手機號碼',
            'mail':'電子信箱',
            'zipcode':'郵遞區號',
            'address':'收件地址',
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

# https://github.com/summernote/django-summernote 新增summernote會使用到