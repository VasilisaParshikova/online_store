from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from shop_app.models import Goods, Category, Order


class Login(LoginView):
    pass
    #template_name = ''


class Logout(LogoutView):
    pass
    #template_name = ''


def registration(request):
    pass
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=password)
#            login(request, user)
            # profile = ProfileForm({'user': user})
        # if profile.is_valid():
        #     profile.save()
        # return redirect('/')
#    else:
#        form = UserCreationForm()
#    return render(request, '', {'form': form})


class MainPage(TemplateView):
    template_name = 'shop_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        category_list = list(Category.objects.all())
        category_dict = dict()
        for item in category_list:
            if item.parent_category:
                category_dict[item.parent_category].append(item)
            else:
                category_dict[item] = []
        context['category'] = category_dict
        print(category_dict.values())
        return context


class Catalog(ListView):
    model = Goods
    #template_name = ''


class Product(DetailView):
    model = Goods
    #template_name = ''


class CategoryView(DetailView):
    model = Category
    #template_name = ''


class Basket(View):
    pass


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


class PersonalPage(DetailView):
    pass


class EditProfile(FormView):
    pass


class OrderHistory(View):
    pass


class OrderPage(DetailView):
    model = Order
