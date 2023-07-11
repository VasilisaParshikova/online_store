from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from orders_app.models import Order, Purchase
from user_app.models import Profile
from shop_app.models import Goods
from copy import deepcopy


class Basket(ListView):
    model = Purchase
    template_name = 'orders_app/busket.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Purchase.objects.select_related('goods').filter(user=self.request.user, order__isnull=True)
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(Basket, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            if self.request.session.get('basket') == None:
                context['object_list'] = []
                context['sum'] = 0
            else:
                object_list = deepcopy(self.request.session['basket'])
                sum = 0
                for obj in object_list:
                    obj['goods'] = Goods.objects.get(id=obj['goods'])
                    sum += int(obj['amount']) * obj['goods'].price
                context['object_list'] = object_list
                context['sum'] = sum
        else:
            item_list = list(context['object_list'])
            sum = 0
            for item in item_list:
                sum += item.amount * item.goods.price
            context['sum'] = sum
        return context


class MakeOrder(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            basket_list = list(Purchase.objects.select_related('goods').filter(user=request.user, order__isnull=True))
            sum = 0
            for item in basket_list:
                sum += item.amount * item.goods.price
        else:
            basket_list = deepcopy(self.request.session['basket'])
            sum = 0
            for obj in basket_list:
                obj['goods'] = Goods.objects.get(id=obj['goods'])
                sum += obj['amount'] * obj['goods'].price

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            return render(request, 'orders_app/order_process.html', {'profile': profile,
                                                                     'basket_list': basket_list, 'sum': sum})
        return render(request, 'orders_app/order_process.html', {'basket_list': basket_list, 'sum': sum})


class MakeOrderPayment(View):
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
    if request.user.is_authenticated:
        basket_list = list(
            Purchase.objects.select_related('goods').filter(user=request.user, order__isnull=True))
        add_to_basket_flag = True
        for obj in basket_list:
            if obj.goods == goods:
                obj.amount += int(request.POST.get('amount'))
                obj.save()
                add_to_basket_flag = False
                break
        if add_to_basket_flag:
            basket_item = Purchase(user=request.user, goods=goods, amount=request.POST.get('amount'))
            basket_item.save()
    else:
        if request.session.get('basket') is None:
            basket_list = [{'goods': goods.id, 'amount': request.POST.get('amount')}]
        else:
            basket_list = request.session['basket']
            add_to_basket_flag = True
            for item in basket_list:
                if item['goods'] == goods.id:
                    item['amount'] += int(request.POST.get('amount'))
                    add_to_basket_flag = False
                    break
            if add_to_basket_flag:
                basket_list.append({'goods': goods.id, 'amount': request.POST.get('amount')})
        request.session['basket'] = basket_list
        request.session.modified = True
    return HttpResponse(status=200)


def add_to_basket_catalog(request):
    goods = Goods.objects.get(id=request.POST.get('id'))
    if request.user.is_authenticated:
        basket_list = list(
            Purchase.objects.select_related('goods').filter(user=request.user, order__isnull=True))
        add_to_basket_flag = True
        for obj in basket_list:
            if obj.goods == goods:
                obj.amount += 1
                obj.save()
                add_to_basket_flag = False
                break
        if add_to_basket_flag:
            basket_item = Purchase(user=request.user, goods=goods, amount=1)
            basket_item.save()
    else:
        if request.session.get('basket') is None:
            basket_list = [{'goods': goods.id, 'amount': 1}]
        else:
            basket_list = request.session['basket']
            add_to_basket_flag = True
            for item in basket_list:
                if item['goods'] == goods.id:
                    item['amount'] += 1
                    add_to_basket_flag = False
                    break
            if add_to_basket_flag:
                basket_list.append({'goods': goods.id, 'amount': 1})
        request.session['basket'] = basket_list
        request.session.modified = True
    return HttpResponse(status=200)


def delete_from_basket(request, pk):
    if request.user.is_authenticated:
        item = Purchase.objects.get(id=pk)
        item.delete()
    else:
        basket_list = request.session['basket']
        for item in basket_list:
            if item['goods'] == pk:
                basket_list.remove(item)
                break
        request.session.modified = True
    return HttpResponseRedirect('/basket')


def remove_item_amount(request):
    if request.user.is_authenticated:
        item = Purchase.objects.get(id=request.POST.get('id'))
        if item.amount == 1:
            item.delete()
        else:
            item.amount = item.amount - 1
            item.save()
    else:
        basket_list = request.session['basket']
        for item in basket_list:
            if item['goods'] == int(request.POST.get('id2')):
                if item['amount'] == 1:
                    basket_list.remove(item)
                    break
                else:
                    item['amount'] -= 1
                    break
        request.session.modified = True
    return HttpResponseRedirect('/basket')


def add_item_amount(request):
    if request.user.is_authenticated:
        item = Purchase.objects.get(id=request.POST.get('id'))
        item.amount = item.amount + 1
        item.save()
    else:
        basket_list = request.session['basket']
        for item in basket_list:
            if item['goods'] == int(request.POST.get('id2')):
                item['amount'] += 1
                break
        request.session.modified = True
    return HttpResponseRedirect('/basket')
