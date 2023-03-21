from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    name = models.CharField(max_length=30, verbose_name='имя')
    patronymic = models.CharField(max_length=30, verbose_name='отчество')
    surname = models.CharField(max_length=50, verbose_name='фамилия')
    avatar = models.ImageField(upload_to='uploads/avatars/', null=True, blank=True, verbose_name='аватар')


class Goods(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    Photo = models.ImageField(upload_to='uploads/products_photo/', null=True, blank=True,
                              verbose_name='изображение товара')
    short_info = models.CharField(max_length=150, verbose_name='краткое описание товара')
    full_info = models.TextField(max_length=1000, verbose_name='полное описание товара')
    price = models.FloatField(verbose_name='цена')
    limited_edition = models.BooleanField(default=False, verbose_name='товар ограниченного тиража')
    sort_index = models.IntegerField(default=0, verbose_name='индекс сортировки')
    was_bought_times = models.IntegerField(default=0, verbose_name='количетсво покупок этого товара')
    category = models.ManyToManyField('Category', on_delete=models.CASCADE, verbose_name='категории')


class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    parent_category = models.ForeignKey('Category', models.SET_NULL, blank=True, null=True, verbose_name='родительская категория')
    image = models.ImageField(upload_to='uploads/categoey_img/', null=True, blank=True, verbose_name='иконка')


class Purchase(models.Model):
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='товар')
    amount = models.IntegerField(verbose_name='количество')
    cost = models.FloatField(verbose_name='стоимость')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='заказ')


class Order(models.Model):
    statuses = {'basket': 'в корзине', 'paid': 'оплачен', 'not_paid': 'не оплачен'}
    purchases = models.ManyToOneRel('Purchase', on_delete=models.CASCADE, verbose_name='покупки')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    delivery = models.ForeignKey('Delivery', on_delete=models.SET_NULL(), verbose_name='доставка')
    status = models.CharField(choices=statuses, default='basket', verbose_name='статус')
    data = models.DateTimeField(auto_now=True, verbose_name='дата заказа')


class Review(models.Model):
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='товар')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    title = models.CharField(max_length=30, verbose_name='заголовок')
    text = models.TextField(max_length=1000, verbose_name='полное описание товара')
    rate = models.IntegerField(default=1, verbose_name='оценка')


class Delivery(models.Model):
    title = models.CharField(max_length=30, verbose_name='название вида доставки')
    price = models.FloatField(verbose_name='стоимость доставки')
    cost_for_free = models.FloatField(verbose_name='минимальная стоимость заказа для бесплатной доставки')

