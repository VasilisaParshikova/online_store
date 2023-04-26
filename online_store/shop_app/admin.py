from django.contrib import admin
from shop_app.models import *

class CategoryAdmin(admin.ModelAdmin):
    pass

class GoodsAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Company, CompanyAdmin)
