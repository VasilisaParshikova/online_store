from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    name = models.CharField(max_length=30, verbose_name='ФИО')
    avatar = models.ImageField(upload_to='uploads/avatars/', null=True, blank=True, verbose_name='аватар')
    phone = models.IntegerField(verbose_name='телефон', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'профайлы'
        verbose_name = 'профайл'

    def __str__(self):
        return f'{self.name} {self.avatar} профайл'
