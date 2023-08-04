from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from shop_app.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:shop_app_category_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:shop_app_category_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


class GoodsAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "price", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:shop_app_goods_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:shop_app_goods_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("title", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:shop_app_company_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:shop_app_company_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("goods", "user", "rate", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:shop_app_review_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:shop_app_review_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Review, ReviewAdmin)
