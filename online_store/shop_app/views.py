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
from django.db.models import Q
from functools import reduce
import operator
from django.http import Http404
from django.utils.translation import gettext as _


class MainPage(TemplateView):
    template_name = "shop_app/index.html"

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        slider = list(
            Goods.objects.order_by("-id").only(
                "title", "price", "short_info", "Photo", "id"
            )[:5]
        )
        limited_edition_list = list(
            Goods.objects.filter(limited_edition=True)
            .select_related("category")
            .only("title", "price", "category", "Photo", "id")[:16]
        )
        top_list = list(
            Goods.objects.order_by("-sort_index", "-was_bought_times")
            .select_related("category")
            .only("title", "Photo", "id", "price", "category")[:8]
        )
        top_category = list(
            Category.objects.filter(id__in=[8, 9, 12])
            .only("title", "image", "id")
            .annotate(min_price=Min("goods__price"))
        )
        context["limited_edition_list"] = limited_edition_list
        context["top_list"] = top_list
        context["slider"] = slider
        context["top_category"] = top_category
        return context


class Catalog(ListView):
    model = Goods
    template_name = "shop_app/catalog.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(Catalog, self).get_context_data(**kwargs)
        objects = self.get_queryset()
        all_goods = Goods.objects.all()
        prices = Goods.objects.aggregate(Max("price"), Min("price"))
        context["min_price"] = prices["price__min"]
        context["max_price"] = prices["price__max"]
        company_list = list(Company.objects.all())
        context["company_list"] = company_list
        if self.request.session.get("sort_type") != None:
            context["sort_type"] = self.request.session["sort_type"]
        if len(objects) == len(all_goods):
            context["category_list"] = Category.objects.filter(
                parent_category__isnull=True
            )
            context["selected_min_price"] = prices["price__min"]
            context["selected_max_price"] = prices["price__max"]
            if self.request.session.get("search_name") != None:
                context["search_name"] = ""
        else:
            selected_companies = []
            categories = []
            for object in objects:
                if object.company and not object.company in selected_companies:
                    selected_companies.append(object.company)
                if (
                    object.category.parent_category
                    and not object.category.parent_category in categories
                ):
                    categories.append(object.category.parent_category)
                if (
                    not object.category.parent_category
                    and not object.category in categories
                ):
                    categories.append(object.category)

            selected_prices = objects.aggregate(Max("price"), Min("price"))
            context["selected_companies"] = selected_companies
            context["selected_min_price"] = selected_prices["price__min"]
            context["selected_max_price"] = selected_prices["price__max"]
            context["category_list"] = categories
            if self.request.session.get("search_name") != None:
                context["search_name"] = self.request.session["search_name"]

        return context

    def get_queryset(self):
        if self.request.method == "POST":
            object_list = Goods.objects.all()
            price = self.request.POST.get("price")
            if price:
                price = [int(x) for x in price.split(";")]
                object_list = object_list.filter(price__range=(price[0], price[1]))
            title = self.request.POST.get("title")

            if title != "":
                self.request.session["search_name"] = title
                title = title.split(" ")
                object_list = object_list.filter(
                    reduce(operator.or_, (Q(title__icontains=x) for x in title))
                )
            companies = self.request.POST.getlist("company")
            if companies:
                object_list = object_list.filter(company__title__in=companies)
            sort_type = self.request.POST.get("sort")
            self.request.session["sort_type"] = sort_type
            if sort_type == "pop":
                object_list = object_list.order_by("-was_bought_times")
            elif sort_type == "price_min":
                object_list = object_list.order_by("price")
            elif sort_type == "price_max":
                object_list = object_list.order_by("-price")
            elif sort_type == "date":
                object_list = object_list.order_by("-id")
            elif sort_type == "review":
                object_list = object_list.annotate(
                    avg_rate=Avg("review__rate")
                ).order_by("-avg_rate")
            return object_list
        if self.request.method == "GET":
            return Goods.objects.all()

    def post(self, *args, **kwargs):
        return super(Catalog, self).get(self.request, *args, **kwargs)


class Product(DetailView):
    model = Goods
    template_name = "shop_app/product.html"

    def post(self, request, pk, *args, **kwargs):
        form = ReviewForm(
            {
                "text": request.POST.get("text"),
                "user": request.user,
                "goods": pk,
                "rate": int(request.POST.get("rate")),
            }
        )
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super(Product, self).get_context_data(**kwargs)
        review_list = list(Review.objects.filter(goods=context["object"]))
        review_amount_avg = Review.objects.filter(goods=context["object"]).aggregate(
            Avg("rate"), Count("id")
        )
        context["review_list"] = review_list
        if review_amount_avg["rate__avg"]:
            context["review_avg"] = round(review_amount_avg["rate__avg"], 1)
        else:
            context["review_avg"] = ""
        context["review_amount"] = review_amount_avg["id__count"]
        return context


class CategoryView(ListView):
    model = Goods
    template_name = "shop_app/catalog_cat.html"
    paginate_by = 12

    def get(self, request, pk, *args, **kwargs):
        self.object_list = self.get_queryset(pk)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data(pk)
        return self.render_to_response(context)

    def get_context_data(self, pk, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        objects = self.get_queryset(pk)
        all_goods = Goods.objects.filter(
            Q(category__id=pk) | Q(category__parent_category__id=pk)
        )
        prices = all_goods.aggregate(Max("price"), Min("price"))
        context["min_price"] = prices["price__min"]
        context["max_price"] = prices["price__max"]
        context["cat_name"] = Category.objects.get(id=pk)
        company_list = []
        for good in all_goods:
            if good.company and not good.company in company_list:
                company_list.append(good.company)
        context["company_list"] = company_list
        if self.request.session.get("sort_type") != None:
            context["sort_type"] = self.request.session["sort_type"]
        if len(objects) == len(all_goods):
            context["category_list"] = Category.objects.filter(
                Q(id=pk) | Q(parent_category__id=pk)
            )
            context["selected_min_price"] = prices["price__min"]
            context["selected_max_price"] = prices["price__max"]
            if self.request.session.get("search_name_cat") != None:
                context["search_name"] = ""
        else:
            selected_companies = []
            categories = []
            for object in objects:
                if object.company and not object.company in selected_companies:
                    selected_companies.append(object.company)
                if object.category and not object.category in categories:
                    categories.append(object.category)
                if (
                    not object.category.parent_category
                    and not object.category in categories
                ):
                    categories.append(object.category)

            selected_prices = objects.aggregate(Max("price"), Min("price"))
            context["selected_companies"] = selected_companies
            context["selected_min_price"] = selected_prices["price__min"]
            context["selected_max_price"] = selected_prices["price__max"]
            context["category_list"] = categories
            if self.request.session.get("search_name_cat") != None:
                context["search_name"] = self.request.session["search_name_cat"]
        return context

    def get_queryset(self, pk):
        if self.request.method == "POST":
            object_list = Goods.objects.filter(
                Q(category__id=pk) | Q(category__parent_category__id=pk)
            )
            price = self.request.POST.get("price")
            if price:
                price = [int(x) for x in price.split(";")]
                object_list = object_list.filter(price__range=(price[0], price[1]))
            title = self.request.POST.get("title")
            if title != "":
                self.request.session["search_name_cat"] = title
                title = title.split(" ")
                object_list = object_list.filter(
                    reduce(operator.or_, (Q(title__icontains=x) for x in title))
                )
            companies = self.request.POST.getlist("company")
            if companies:
                object_list = object_list.filter(company__title__in=companies)
            sort_type = self.request.POST.get("sort")
            self.request.session["sort_type"] = sort_type
            if sort_type == "pop":
                object_list = object_list.order_by("-was_bought_times")
            elif sort_type == "price_min":
                object_list = object_list.order_by("price")
            elif sort_type == "price_max":
                object_list = object_list.order_by("-price")
            elif sort_type == "date":
                object_list = object_list.order_by("-id")
            elif sort_type == "review":
                object_list = object_list.annotate(
                    avg_rate=Avg("review__rate")
                ).order_by("-avg_rate")
            return object_list
        if self.request.method == "GET":
            return Goods.objects.filter(
                Q(category__id=pk) | Q(category__parent_category__id=pk)
            )

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")

        return self.get(self.request, pk)
