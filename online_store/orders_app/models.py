from django.db import models
from django.contrib.auth.models import User
from shop_app.models import Goods


class Purchase(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='товар')
    amount = models.IntegerField(verbose_name='количество')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='заказ', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'покупки'
        verbose_name = 'покупка'

    def __str__(self):
        return f'{self.goods} куплено {self.user}'


class Order(models.Model):
    statuses = [('paid', 'оплачен'), ('not_paid', 'не оплачен')]
    payments = [('card', 'Онлйан карта'), ('random_card', 'Рандомная карта')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    delivery = models.ForeignKey('Delivery', on_delete=models.SET_NULL, verbose_name='доставка', null=True, blank=True)
    status = models.CharField(choices=statuses, max_length=30, default='basket', verbose_name='статус')
    data = models.DateField(auto_now_add=True, verbose_name='дата заказа')
    cost = models.IntegerField(verbose_name='стоимость')
    payment_type = models.CharField(choices=payments, max_length=30, default='card', verbose_name='тип доставки',
                                    null=True, blank=True)
    city = models.CharField(max_length=30, verbose_name='город доставки', null=True, blank=True)
    address = models.CharField(max_length=1000, verbose_name='адрес', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'заказы'
        verbose_name = 'заказ'

    def __str__(self):
        return f'заказ {self.id} от {self.data} пользователя {self.user}'


class Delivery(models.Model):
    title = models.CharField(max_length=30, verbose_name='название вида доставки')
    price = models.FloatField(verbose_name='стоимость доставки')
    cost_for_free = models.FloatField(verbose_name='минимальная стоимость заказа для бесплатной доставки')

    class Meta:
        verbose_name_plural = 'доставки'
        verbose_name = 'доставка'

    def __str__(self):
        return self.title
