from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from orders_app.models import Order, Purchase
from user_app.models import Profile
from shop_app.models import Goods

class Basket(ListView):
    model = Purchase
    template_name = 'orders_app/busket.html'

    def get_queryset(self):
        return Purchase.objects.select_related('goods').filter(user=self.request.user, order__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(Basket, self).get_context_data(**kwargs)
        item_list = list(context['object_list'])
        print(item_list)
        sum = 0
        for item in item_list:
            sum += item.amount * item.goods.price
        context['sum'] = sum
        return context


class MakeOrderInfo(View):
    pass


class MakeOrderDelivery(View):
    pass


class MakeOrderPaymentType(View):
    pass


class MakeOrderPayment(View):
    pass


class MakeOrderConformation(View):
    pass


class OrderHistory(ListView):
    model = Order
    template_name = 'orders_app/order_history.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-data').only('id', 'data', 'delivery',
                                                                                   'status', 'cost',
                                                                                   'payment_type')


class OrderPage(DetailView):
    model = Order
    template_name = 'orders_app/order_page.html'

    def get_context_data(self, **kwargs):
        context = super(OrderPage, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        items_list = list(Purchase.objects.select_related('goods').only('goods', 'amount').filter(order=self.object))
        context['profile'] = profile
        context['items_list'] = items_list
        return context

def add_to_basket(request, pk):
    goods = Goods.objects.get(id=pk)
    basket_item = Purchase(user=request.user, goods=goods, amount=request.POST.get('amount'))
    basket_item.save()
    return HttpResponse(status=200)


def add_to_basket_catalog(request):
    print('@@@@@@@@@@@')
    goods = Goods.objects.get(id=request.POST.get('id'))
    basket_item = Purchase(user=request.user, goods=goods, amount=1)
    basket_item.save()
    return HttpResponse(status=200)