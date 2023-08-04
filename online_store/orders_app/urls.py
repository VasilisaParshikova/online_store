from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("basket", views.Basket.as_view(), name="basket"),
    path("makeorder", views.MakeOrder.as_view(), name="make_order"),
    path(
        "makeorder/payment<int:pk>",
        views.MakeOrderPayment.as_view(),
        name="make_order_payment",
    ),
    path("lk/orderhistory", views.OrderHistory.as_view(), name="order_history"),
    path("lk/order<int:pk>", views.OrderPage.as_view(), name="order_page"),
    path(
        "catalog/product<int:pk>/modal_open",
        views.add_to_basket,
        name="product_page_modal",
    ),
    path("add_item", views.add_to_basket_catalog, name="catalog_page_modal"),
    path("delate<int:pk>", views.delete_from_basket, name="delete_from_basket"),
    path("remove_item_amount", views.remove_item_amount, name="remove_item_amount"),
    path("add_item_amount", views.add_item_amount, name="add_item_amount"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
