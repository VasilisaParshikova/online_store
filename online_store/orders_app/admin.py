from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from orders_app.models import *


class AdminPurchase(admin.ModelAdmin):
    list_display = ("goods", "user", "amount", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:orders_app_purchase_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:orders_app_purchase_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


class AdminOrder(admin.ModelAdmin):
    list_display = ("id", "user", "data", "status", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:orders_app_order_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:orders_app_order_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


class AdminDelivery(admin.ModelAdmin):
    list_display = ("title", "price", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:orders_app_delivery_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:orders_app_delivery_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


admin.site.register(Purchase, AdminPurchase)
admin.site.register(Order, AdminOrder)
admin.site.register(Delivery, AdminDelivery)
