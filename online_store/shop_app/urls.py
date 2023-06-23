from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('catalog', views.Catalog.as_view(), name='catalog'),
    path('catalog/product<int:pk>', views.Product.as_view(), name='product_page'),
    path('catalog/category<int:pk>', views.CategoryView.as_view(), name='category_page')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)