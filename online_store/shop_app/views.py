from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from shop_app.models import Goods, Category, Company, Review
from django.db.models import Max, Min, Avg, Count
from shop_app.forms import ReviewForm


class MainPage(TemplateView):
    template_name = 'shop_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        slider = list(Goods.objects.order_by('-id').only(
            'title', 'price', 'short_info', 'Photo', 'id')[:5])
        limited_edition_list = list(Goods.objects.filter(limited_edition=True).select_related('category').only(
            'title', 'price', 'category', 'Photo', 'id')[:16])
        top_list = list(Goods.objects.order_by('-sort_index', '-was_bought_times').select_related('category').only(
            'title', 'Photo', 'id', 'price', 'category')[:8])
        top_category = list(Category.objects.filter(id__in=[8, 9, 12]).only('title', 'image', 'id').annotate(min_price=Min('goods__price')))
        context['limited_edition_list'] = limited_edition_list
        context['top_list'] = top_list
        context['slider'] = slider
        context['top_category'] = top_category
        return context


class Catalog(ListView):
    model = Goods
    template_name = 'shop_app/catalog.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(Catalog, self).get_context_data(**kwargs)
        company_list = list(Company.objects.all())
        prices = Goods.objects.aggregate(Max('price'), Min('price'))
        context['company_list'] = company_list
        context['min_price'] = prices['price__min']
        context['max_price'] = prices['price__max']
        return context


class Product(DetailView):
    model = Goods
    template_name = 'shop_app/product.html'

    def post(self, request, pk, *args, **kwargs):
        form = ReviewForm({'text': request.POST.get('text'),
                           'user': request.user,
                           'goods': pk,
                           'rate': int(request.POST.get('rate'))})
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super(Product, self).get_context_data(**kwargs)
        review_list = list(Review.objects.filter(goods=context['object']))
        review_amount_avg = Review.objects.filter(goods=context['object']).aggregate(Avg('rate'), Count('id'))
        context['review_list'] = review_list
        if review_amount_avg['rate__avg']:
            context['review_avg'] = round(review_amount_avg['rate__avg'], 1)
        else:
            context['review_avg'] = ''
        context['review_amount'] = review_amount_avg['id__count']
        return context


class CategoryView(DetailView):
    model = Category
    #template_name = ''



