# Generated by Django 4.1.7 on 2023-05-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='patronymic',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='surname',
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=30, verbose_name='ФИО'),
        ),
    ]
