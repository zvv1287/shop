from django import template

from mainapp.models import ProductCategory
from basketapp.models import Basket

register = template.Library()


@register.inclusion_tag('include/sidebar.html', takes_context=True)
def categories_list(context):
    """template tag вывода категорий"""
    categories = ProductCategory.objects.all()
    print(categories)
    return {"categories_list": categories}


@register.inclusion_tag('include/mini_basket.html', takes_context=True)
def mini_basket(context):
    """template tag вывода кол-во товаров и суммы в корзине"""
    request = context.request
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)
        if user_basket:
            total_sum = sum(basket.sum() for basket in user_basket)
            total_quantity = sum(basket.quantity for basket in user_basket)
            return {'basket': f'В корзине {total_quantity} товар(-ов) на сумму {total_sum} руб.', 'user': request.user}
        return {'basket': 'Корзина пуста'}

    return {'basket': ''}
