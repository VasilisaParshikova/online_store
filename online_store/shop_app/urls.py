from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('registration', views.registration, name='registration'),
    path('catalog', views.Catalog.as_view(), name='catalog'),
    path('catalog/product<int:pk>', views.Product.as_view(), name='product_page'),
    path('catalog/category<int:pk>', views.Category.as_view(), name='category_page'),
    path('basket', views.Basket.as_view(), name='basket'),
    path('makeorder', views.MakeOrderInfo.as_view(), name='make_order_info'),
    path('makeorder/delivery', views.MakeOrderDelivery.as_view(), name='make_order_delivery'),
    path('makeorder/paymentchoice', views.MakeOrderPaymentType.as_view(), name='make_order_payment_choice'),
    path('makeorder/conformation', views.MakeOrderConformation.as_view(), name='make_order_conformation'),
    path('makeorder/payment', views.MakeOrderPayment.as_view(), name='make_order_payment'),
    path('lk', views.PersonalPage.as_view(), name='personal_page'),
    path('lk/edit', views.EditProfile.as_view(), name='edit_profile'),
    path('lk/orderhostiry', views.OrderHistory.as_view(), name='order_history'),
    path('lk/order<int:pk>', views.OrderPage.as_view(), name='order_page')
]