# Generated by Django 4.1.7 on 2023-06-09 12:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders_app', '0004_alter_order_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата заказа'),
        ),
    ]
