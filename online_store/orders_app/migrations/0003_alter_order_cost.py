# Generated by Django 4.1.7 on 2023-06-09 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders_app', '0002_remove_purchase_cost_order_address_order_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.IntegerField(verbose_name='стоимость'),
        ),
    ]
