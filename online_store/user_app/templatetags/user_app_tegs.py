from django import template
from shop_app.models import Category
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def category_dict_get():
    category_list = list(Category.objects.all())
    category_dict = dict()
    for item in category_list:
        if item.parent_category:
            category_dict[item.parent_category].append(item)
        else:
            category_dict[item] = []
    cache.get_or_set('category', category_dict, 3600)
    return category_dict
