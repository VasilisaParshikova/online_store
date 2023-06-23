from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Goods(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    Photo = models.ImageField(upload_to='uploads/products_photo/', null=True, blank=True,
                              verbose_name='изображение товара')
    short_info = models.CharField(max_length=150, verbose_name='краткое описание товара')
    full_info = models.TextField(max_length=10000, verbose_name='полное описание товара')
    price = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='цена')
    limited_edition = models.BooleanField(default=False, verbose_name='товар ограниченного тиража')
    sort_index = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)],
                                     verbose_name='индекс сортировки')
    was_bought_times = models.IntegerField(default=0, verbose_name='количетсво покупок этого товара')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='категории')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='компания производитель')

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товары'

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')

    class Meta:
        verbose_name_plural = 'фирмы'
        verbose_name = 'фирма'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    parent_category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name='родительская категория')
    image = models.ImageField(upload_to='uploads/categoey_img/', null=True, blank=True, verbose_name='иконка')

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'

    def __str__(self):
        return self.title


class Review(models.Model):
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.TextField(max_length=1000, verbose_name='текст отзыва')
    rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                               verbose_name='оценка')

    class Meta:
        verbose_name_plural = 'отзывы'
        verbose_name = 'отзыв'

    def __str__(self):
        return f'Отзыв о {self.goods}'
