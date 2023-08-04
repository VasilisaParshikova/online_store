import json

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from user_app.models import Profile
from user_app.forms import LoginForm, ProfileForm, ProfileEditForm
from django.contrib.auth.forms import UserCreationForm
from shop_app.models import Goods, Category, Company, Review
from orders_app.models import Purchase, Order, Delivery
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth.forms import SetPasswordForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.session.get("basket"):
                        basket_list = list(
                            Purchase.objects.select_related("goods").filter(
                                user=request.user, order__isnull=True
                            )
                        )
                        for item in request.session.get("basket"):
                            goods = Goods.objects.get(id=item["goods"])
                            add_to_basket_flag = True
                            for obj in basket_list:
                                if obj.goods == goods:
                                    obj.amount += item["amount"]
                                    obj.save()
                                    add_to_basket_flag = False
                                    break
                            if add_to_basket_flag:
                                basket_item = Purchase(
                                    user=user, goods=goods, amount=item["amount"]
                                )
                                basket_item.save()
                    return HttpResponseRedirect("/")
                else:
                    return render(
                        request,
                        "user_app/login.html",
                        {"error": "Неверно введён e-mail или пароль"},
                    )
            else:
                return render(
                    request,
                    "user_app/login.html",
                    {"error": "Неверно введён e-mail или пароль"},
                )
        else:
            return render(
                request,
                "user_app/login.html",
                {"error": "Неверно введён e-mail или пароль"},
            )
    return render(request, "user_app/login.html")


def user_login_1(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.session.get("basket"):
                        basket_list = list(
                            Purchase.objects.select_related("goods").filter(
                                user=request.user, order__isnull=True
                            )
                        )
                        for item in request.session.get("basket"):
                            goods = Goods.objects.get(id=item["goods"])
                            add_to_basket_flag = True
                            for obj in basket_list:
                                if obj.goods == goods:
                                    obj.amount += item["amount"]
                                    obj.save()
                                    add_to_basket_flag = False
                                    break
                            if add_to_basket_flag:
                                basket_item = Purchase(
                                    user=user, goods=goods, amount=item["amount"]
                                )
                                basket_item.save()
                    return HttpResponseRedirect("/makeorder")
                else:
                    return render(
                        request,
                        "user_app/login.html",
                        {"error": "Неверно введён e-mail или пароль"},
                    )
            else:
                return render(
                    request,
                    "user_app/login.html",
                    {"error": "Неверно введён e-mail или пароль"},
                )
        else:
            return render(
                request,
                "user_app/login.html",
                {"error": "Неверно введён e-mail или пароль"},
            )
    return render(request, "user_app/login.html")


class Logout(LogoutView):
    template_name = "user_app/logout.html"


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            name = request.POST.get("first_name")
            user = authenticate(username=username, password=password)
            login(request, user)
            user.email = username
            user.save(update_fields=["email"])
            profile = ProfileForm({"user": user, "name": name})
            if profile.is_valid():
                profile.save()
            else:
                error = "Возникла ошибка регистрации. Проверьте введённые данные"
                return render(request, "user_app/registration.html", {"error": error})
            if request.session.get("basket"):
                for item in request.session.get("basket"):
                    goods = Goods.objects.get(id=item["goods"])
                    basket_item = Purchase(
                        user=user, goods=goods, amount=item["amount"]
                    )
                    basket_item.save()
            return HttpResponseRedirect("/")
        else:
            error = form.errors
            return render(request, "user_app/registration.html", {"error": error})
    else:
        form = UserCreationForm()
    return render(request, "user_app/registration.html", {"form": form})


def reg_in_order(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        phone = request.POST.get("phone")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            name = request.POST.get("first_name")
            user = authenticate(username=username, password=password)
            login(request, user)
            user.email = username
            user.save(update_fields=["email"])
            profile = ProfileForm({"user": user, "name": name, "phone": phone})
            if profile.is_valid():
                profile.save()
            else:
                error = "Возникла ошибка регистрации. Проверьте введённые данные"
                error = {"error": error, "flag": True}
                return JsonResponse(error)
            if request.session.get("basket"):
                for item in request.session.get("basket"):
                    goods = Goods.objects.get(id=item["goods"])
                    basket_item = Purchase(
                        user=user, goods=goods, amount=item["amount"]
                    )
                    basket_item.save()
            return HttpResponseRedirect("/makeorder")
        else:
            error = ""
            for k, v in form.errors.items():
                error += k + ": " + str(v)[26:-10] + "<br/>"
            error = {"error": error, "flag": True}
            return JsonResponse(error)
    else:
        form = UserCreationForm()
    return render(request, "user_app/registration.html", {"form": form})


class PersonalPage(TemplateView):
    template_name = "user_app/lk.html"

    def get_context_data(self, **kwargs):
        context = super(PersonalPage, self).get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = ProfileForm(
                {"user": self.request.user, "name": "Укажите ваши ФИО"}
            )
            profile.save()
        context["object"] = profile
        try:
            last_order = (
                Order.objects.filter(user=self.request.user)
                .only("id", "data", "delivery", "status", "cost", "payment_type")
                .latest("id")
            )
        except Order.DoesNotExist:
            last_order = []
        if not last_order == []:
            context["last_order"] = last_order
        return context


def edit_profile(request):
    context = {}
    profile = Profile.objects.get(user=request.user.id)
    context["object"] = profile

    if request.method == "POST":
        if request.POST.get("password2"):
            if request.POST.get("password2") == request.POST.get("password1"):
                usermane = request.user.username
                password = request.POST.get("password1")
                request.user.set_password(request.POST.get("password1"))
                request.user.save()
                user = authenticate(username=usermane, password=password)
                login(request, user)
        if request.POST.get("email"):
            request.user.email = request.POST.get("email")
            request.user.username = request.POST.get("email")
            password = request.user.password
            request.user.save(update_fields=["email", "username"])
            user = authenticate(username=request.POST.get("email"), password=password)
            login(request, user)
        print(request.FILES)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return HttpResponseRedirect(request.path_info)

    return render(request, "user_app/Profile_update.html", context)
