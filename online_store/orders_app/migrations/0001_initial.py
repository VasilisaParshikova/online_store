# Generated by Django 4.1.7 on 2023-05-15 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('shop_app', '0005_remove_order_delivery_remove_order_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='название вида доставки')),
                ('price', models.FloatField(verbose_name='стоимость доставки')),
                ('cost_for_free',
                 models.FloatField(verbose_name='минимальная стоимость заказа для бесплатной доставки')),
            ],
            options={
                'verbose_name': 'доставка',
                'verbose_name_plural': 'доставки',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status',
                 models.CharField(choices=[('basket', 'в корзине'), ('paid', 'оплачен'), ('not_paid', 'не оплачен')],
                                  default='basket', max_length=30, verbose_name='статус')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='дата заказа')),
                ('delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to='orders_app.delivery', verbose_name='доставка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='количество')),
                ('cost', models.FloatField(verbose_name='стоимость')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.goods',
                                            verbose_name='товар')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders_app.order',
                                            verbose_name='заказ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'покупка',
                'verbose_name_plural': 'покупки',
            },
        ),
    ]
