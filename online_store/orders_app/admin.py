from django.contrib import admin
from orders_app.models import *


class ProfilePurchase(admin.ModelAdmin):
    pass


class ProfileOrder(admin.ModelAdmin):
    pass


class ProfileDelivery(admin.ModelAdmin):
    pass


admin.site.register(Purchase, ProfilePurchase)
admin.site.register(Order, ProfileOrder)
admin.site.register(Delivery, ProfileDelivery)
