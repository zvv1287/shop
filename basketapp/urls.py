from django.urls import path

from basketapp.views import basket_add, basket_remove, basket_edit

app_name = 'basketapp'

urlpatterns = [
    path('basketapp-add/<int:product_id>/', basket_add, name='basket_add'),
    path('basketapp-remove/<int:id>/', basket_remove, name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
