# Generated by Django 4.1.2 on 2022-10-28 03:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("home_board", models.TextField(max_length=500, verbose_name="首頁公布欄")),
                (
                    "checkout_board",
                    models.TextField(max_length=500, verbose_name="結帳公布欄"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Carousel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="主標"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=200, null=True, verbose_name="描述"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="carousel", verbose_name="圖片"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="優惠券名稱")),
                ("code", models.CharField(max_length=10, verbose_name="優惠碼")),
                ("discount", models.IntegerField(verbose_name="折扣費用")),
                ("valid_from", models.DateTimeField(verbose_name="開始日期")),
                ("valid_to", models.DateTimeField(verbose_name="結束日期")),
                ("active", models.BooleanField(verbose_name="啟用")),
            ],
        ),
        migrations.CreateModel(
            name="DeliverCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=10, verbose_name="運送方式")),
                ("fee", models.IntegerField(verbose_name="運費")),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="訂單編號",
                    ),
                ),
                ("name", models.CharField(max_length=10, verbose_name="收件人")),
                ("phone", models.CharField(max_length=12, verbose_name="手機號碼")),
                (
                    "mail",
                    models.EmailField(max_length=254, null=True, verbose_name="電子信箱"),
                ),
                (
                    "zipcode",
                    models.CharField(
                        blank=True, max_length=6, null=True, verbose_name="郵遞區號"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="地址"
                    ),
                ),
                (
                    "delivery_company",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="運送超市"
                    ),
                ),
                (
                    "delivery_store",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="店到店門市"
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="備註欄"
                    ),
                ),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                (
                    "delivery_price",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="運費"
                    ),
                ),
                (
                    "coupon_price",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="優惠卷折扣"
                    ),
                ),
                (
                    "total_price",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="結帳金額"
                    ),
                ),
                (
                    "transfer",
                    models.CharField(
                        choices=[("是", "是"), ("否", "否")],
                        default="否",
                        max_length=20,
                        verbose_name="收到款項",
                    ),
                ),
                (
                    "complete",
                    models.CharField(
                        choices=[("是", "是"), ("否", "否")],
                        default="否",
                        max_length=20,
                        verbose_name="已寄出訂單",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transfername", models.CharField(max_length=10, verbose_name="匯款人姓名")),
                ("transferNums", models.CharField(max_length=15, verbose_name="帳號後五碼")),
                ("transferPrice", models.CharField(max_length=15, verbose_name="匯款金額")),
                ("transferdate", models.CharField(max_length=15, verbose_name="匯款日期")),
                (
                    "sendingdate",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="填表單日期"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40, verbose_name="產品名")),
                ("price", models.IntegerField(verbose_name="原價")),
                ("promotion", models.IntegerField(verbose_name="特價")),
                ("detail", models.TextField(max_length=700, verbose_name="商品說明")),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="product", verbose_name="圖片"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.FileField(upload_to="images")),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(blank=True, default=0, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Delivery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "delivery",
                    models.ManyToManyField(
                        to="shop.delivercompany", verbose_name="選擇送貨方式"
                    ),
                ),
            ],
        ),
    ]
