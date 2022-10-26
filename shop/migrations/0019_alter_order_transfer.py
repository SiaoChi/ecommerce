# Generated by Django 4.1.2 on 2022-10-23 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0018_rename_transdatetime_paymentreport_sendingdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transfer",
            field=models.BooleanField(
                choices=[(True, "是"), (False, "否")], default=False, verbose_name="收到款項"
            ),
        ),
    ]