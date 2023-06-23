from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('basket', views.Basket.as_view(), name='basket'),
    path('makeorder', views.MakeOrderInfo.as_view(), name='make_order_info'),
    path('makeorder/delivery', views.MakeOrderDelivery.as_view(), name='make_order_delivery'),
    path('makeorder/paymentchoice', views.MakeOrderPaymentType.as_view(), name='make_order_payment_choice'),
    path('makeorder/conformation', views.MakeOrderConformation.as_view(), name='make_order_conformation'),
    path('makeorder/payment', views.MakeOrderPayment.as_view(), name='make_order_payment'),
    path('lk/orderhistory', views.OrderHistory.as_view(), name='order_history'),
    path('lk/order<int:pk>', views.OrderPage.as_view(), name='order_page'),
    path('catalog/product<int:pk>/modal_open', views.add_to_basket, name='product_page_modal'),
    path('add_item', views.add_to_basket_catalog, name='catalog_page_modal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)