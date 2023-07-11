from django import template
from shop_app.models import Category
from orders_app.models import Purchase, Goods
from django.core.cache import cache
from django.db.models import Sum

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

@register.simple_tag
def basket_amount(request):
    if request.user.is_authenticated:
        list_item = Purchase.objects.filter(user=request.user.id, order__isnull=True).aggregate(Sum('amount'))
        amount = list_item['amount__sum']
    else:
        if request.session.get('basket'):
            items_list = request.session['basket']
            amount = 0
            for item in items_list:
                amount += int(item['amount'])
        else:
            amount = 0
    cache.get_or_set('basket_amount', amount, 600)
    return amount

@register.simple_tag
def basket_cost(request):
    if request.user.is_authenticated:
        item_list = list(Purchase.objects.select_related('goods').filter(user=request.user.id, order__isnull=True))
        sum = 0
        for item in item_list:
            sum += item.amount * item.goods.price
    else:
        if request.session.get('basket'):
            items_list = request.session['basket']
            sum = 0
            for item in items_list:
                sum += int(item['amount']) * Goods.objects.get(id=item['goods']).price
        else:
            sum = 0
    cache.get_or_set('basket_sum', sum, 600)
    return sum