# Generated by Django 4.1.7 on 2023-04-21 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goods",
            name="category",
        ),
        migrations.AddField(
            model_name="goods",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop_app.category",
                verbose_name="категории",
            ),
            preserve_default=False,
        ),
    ]
