from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from mainapp.models import Product
from basketapp.models import Basket


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    """Реализован ajax по js скрипту static/js/basket.js"""
    if request.is_ajax():
        quantity = int(quantity)

        basket = Basket.objects.get(id=int(id))
        message = ''
        if not (basket.product.quantity == 0 and quantity > basket.quantity):
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()
        else:
            message = f'Товар: {basket.product} - закончился'
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets,
            'message': message
        }
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})
