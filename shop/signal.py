from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings
from .until import cookieCart


def createOrder(sender, instance, created, **kwargs):
    if created:
        cartdata = cookieCart(request)
        cartItems = cartdata['cartItems']
        order = cartdata['order']
        items = cartdata['items']
        order = instance

        subject = '嘻嘻選物 - 我們已經收到您的訂單，再麻煩您注意匯款時間'
        message = ' 以下是您的購物清單  ' \
                {% for item in items}
                {{item.product}}

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            # 這裡的user抓取的關鍵是user=instance
            [order.email],
            fail_silently=False,
        )

post_save.connect(createOrder, sender='嘻嘻')