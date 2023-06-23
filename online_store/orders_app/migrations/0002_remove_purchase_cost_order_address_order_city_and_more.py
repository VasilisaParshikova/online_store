# Generated by Django 4.1.7 on 2023-06-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='cost',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='qwerty', max_length=1000, verbose_name='адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='qwerty', max_length=30, verbose_name='город доставки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.FloatField(default=19999, verbose_name='стоимость'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('card', 'Онлйан карта'), ('random_card', 'Рандомная карта')],
                                   default='card', max_length=30, verbose_name='тип доставки'),
        ),
    ]
