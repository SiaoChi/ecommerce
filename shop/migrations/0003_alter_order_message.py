# Generated by Django 4.1 on 2022-09-17 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="message",
            field=models.TextField(max_length=500, null=True, verbose_name="備註欄"),
        ),
    ]
