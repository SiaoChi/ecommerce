from .models import *
from django.forms import ModelForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ="__all__"
        exclude = ['datetime', 'complete']
        widgets = {

        }
        labels = {
            'name':'收件姓名',
            'phone':'手機號碼',
            'mail':'電子信箱',
            'zipcode':'郵遞區號',
            'address':'收件地址',
            'message':'留言備註',
        }

        def __init__(self, *args, **kwargs):
            super(OrderForm, self).__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
