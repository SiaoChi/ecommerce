# Generated by Django 4.1.2 on 2022-10-23 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0017_remove_paymentreport_datetime_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paymentreport",
            old_name="transdatetime",
            new_name="sendingdate",
        ),
    ]