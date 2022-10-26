# Generated by Django 4.1.2 on 2022-10-23 10:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0016_paymentreport_datetime_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="paymentreport", name="datetime",),
        migrations.AddField(
            model_name="paymentreport",
            name="transdatetime",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="填表單日期"
            ),
        ),
    ]
