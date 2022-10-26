from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

class PaymentReportAdmin(admin.ModelAdmin):
    ordering = ('-sendingdate',)
    search_fields = ('transferNums',)
    class Meta:
        model = PaymentReport

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product

class summerAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

class OrderItemAdmin(admin.StackedInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    ordering = ('-datetime',)
    # list_display = ('datetime',)
    search_fields = ('id',)
    inlines = [OrderItemAdmin]

    class Meta:
        model = Order


admin.site.register(Carousel)
admin.site.register(Product,summerAdmin)
admin.site.register(Order,OrderAdmin)
# admin.site.register(OrderItem)
admin.site.register(Board,summerAdmin)
admin.site.register(Coupon)
admin.site.register(Delivery)
admin.site.register(DeliverCompany)
admin.site.register(PaymentReport,PaymentReportAdmin)



