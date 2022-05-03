from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404

from authapp.models import User
from mainapp.models import Product, ProductCategory
from adminapp.forms import AdminUserProfileForm, AdminUserRegisterForm, AdminProductsProfileForm, \
    AdminCategoriesProfileForm, AdminOrderForm
from ordersapp.models import Order
from ordersapp.views import OrderItemsUpdate


@user_passes_test(lambda u: u.is_superuser, login_url='mainapp:products')
def index(request):
    return render(request, 'adminapp/index.html', {'title': 'Админ'})


class AdminListView(ListView):
    """Вывод списка всех пользователей, категорий товаров или товаров"""

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['model'] == 'user':
            self.model = User
            self.template_name = 'adminapp/admins_user_read.html'
        elif self.kwargs['model'] == 'categories':
            self.model = ProductCategory
            self.template_name = 'adminapp/admin_categories_read.html'
        elif self.kwargs['model'] == 'products':
            self.model = Product
            self.template_name = 'adminapp/admin_products_read.html'
        else:
            raise Http404
        return super(AdminListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        if self.model == User:
            context['title'] = 'Пользователи'

        elif self.model == ProductCategory:
            context['title'] = 'Категории'

        elif self.model == Product:
            context['title'] = 'Продукты'
        return context


class AdminCreateView(CreateView):
    """Создание пользователя, категории товаров или товара"""

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):

        if self.kwargs['model'] == 'user':
            self.model = User
            self.template_name = 'adminapp/admin_users_create.html'
            self.form_class = AdminUserRegisterForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['user'])

        elif self.kwargs['model'] == 'categories':
            self.model = ProductCategory
            self.template_name = 'adminapp/admin_categories_create.html'
            self.form_class = AdminCategoriesProfileForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['categories'])

        elif self.kwargs['model'] == 'products':
            self.model = Product
            self.template_name = 'adminapp/admin_products_create.html'
            self.form_class = AdminProductsProfileForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['products'])
        else:
            raise Http404

        return super(AdminCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminCreateView, self).get_context_data(**kwargs)
        if self.model == User:
            context['title'] = 'Новый пользователь'

        elif self.model == ProductCategory:
            context['title'] = 'Добавить категорию'

        elif self.model == Product:
            context['title'] = 'Добавить продукт'
        return context


class AdminUpdateView(UpdateView):
    """Редактирование пользователя, категории товаров или товара"""

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):

        if self.kwargs['model'] == 'user':
            self.model = User
            self.template_name = 'adminapp/admin_user_update_delete.html'
            self.form_class = AdminUserProfileForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['user'])

        elif self.kwargs['model'] == 'categories':
            self.model = ProductCategory
            self.template_name = 'adminapp/admins_categories_update_delete.html'
            self.form_class = AdminCategoriesProfileForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['categories'])

        elif self.kwargs['model'] == 'products':
            self.model = Product
            self.template_name = 'adminapp/admins_products_update_delete.html'
            self.form_class = AdminProductsProfileForm
            self.success_url = reverse_lazy('adminapp:admins_read', args=['products'])
        else:
            raise Http404

        return super(AdminUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminUpdateView, self).get_context_data(**kwargs)
        if self.model == User:
            context['title'] = 'Редактирование пользователя'

        elif self.model == ProductCategory:
            context['title'] = 'Редактирование категории'

        elif self.model == Product:
            context['title'] = 'Редактирование продукта'
        return context


class AdminDeleteView(DeleteView):
    """Удаление пользователя, категории товаров или товара"""

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['model'] == 'user':
            self.model = User
            self.template_name = 'adminapp/admin_user_update_delete.html'
            self.success_url = reverse_lazy('adminapp:admins_read', args=['user'])

        elif self.kwargs['model'] == 'categories':
            self.model = ProductCategory
            self.template_name = 'adminapp/admins_categories_update_delete.html'
            self.success_url = reverse_lazy('adminapp:admins_read', args=['categories'])

        elif self.kwargs['model'] == 'products':
            self.model = Product
            self.template_name = 'adminapp/admins_products_update_delete.html'
            self.success_url = reverse_lazy('adminapp:admins_read', args=['products'])
        else:
            raise Http404

        return super(AdminDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.model == User:
            self.object = self.get_object()
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        elif self.model == ProductCategory:
            return super(AdminDeleteView, self).delete(request, *args, **kwargs)
        elif self.model == Product:
            return super(AdminDeleteView, self).delete(request, *args, **kwargs)


class OrderList(ListView):
    """Список заказов"""
    model = Order
    template_name = 'adminapp/admins_order_read.html'

    def get_queryset(self):
        return Order.objects.all()

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdminOrderItemsUpdate(OrderItemsUpdate):
    """Редактирование заказа"""
    fields = None
    template_name = 'adminapp/admin_order_detail.html'
    form_class = AdminOrderForm
    success_url = reverse_lazy('adminapp:admin_orders_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdminOrderDelete(DeleteView):
    """Удаление заказа. Делает его не активным."""

    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
