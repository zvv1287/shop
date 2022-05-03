from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.base import View

from mainapp.models import Product, ProductCategory


class IndexView(View):

    def get(self, request):
        context = {
            'head': 'Shop - главная',
        }
        return render(request, 'mainapp/index.html', context)


class ProductsView(View):

    def get(self, request, slug=None):

        if not slug:
            category_name = ''
            cards = Product.objects.all()
        else:
            category_name = ProductCategory.objects.get(slug=slug)
            cards = Product.objects.filter(category=category_name)

        page = request.GET.get('page', 1)
        products_on_page = 6
        paginator = Paginator(cards, products_on_page)

        context = {
            'head': 'My_Shop - каталог',
            'cards': paginator.page(page),
            'category_name': category_name,
        }
        return render(request, 'mainapp/products.html', context)
