from django.urls import path
from mainapp.views import IndexView, ProductsView


app_name = 'mainapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductsView.as_view(), name='product'),
]


