from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from user_app.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name", "del_link", "change_link")

    def del_link(self, obj):
        url = reverse("admin:user_app_profile_delete", args=(obj.id,))

        return format_html('<a href="{}">Удалить</a>', url)

    del_link.short_description = " "

    def change_link(self, obj):
        url = reverse("admin:user_app_profile_change", args=(obj.id,))

        return format_html('<a href="{}">Изменить</a>', url)

    change_link.short_description = " "


admin.site.register(Profile, ProfileAdmin)
