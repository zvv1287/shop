from authapp.forms import UserRegisterForm, UserProfileForm
from django import forms
from mainapp.models import Product, ProductCategory
from authapp.models import User
from ordersapp.models import Order


class AdminUserRegisterForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'avatar', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AdminUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'


class AdminUserProfileForm(UserProfileForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'avatar', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AdminUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = False
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'


class AdminProductsProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'short_description', 'price', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(AdminProductsProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название продукта'
        self.fields['image'].widget.attrs['placeholder'] = 'Загрузите изображение продукта'
        self.fields['description'].widget.attrs['placeholder'] = 'Полное описание продукта'
        self.fields['short_description'].widget.attrs['placeholder'] = 'Краткое описание продукта'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Укажите кол-во'
        self.fields['category'].widget.attrs['placeholder'] = 'Укажите категорию продукта'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class AdminCategoriesProfileForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'slug')

    def __init__(self, *args, **kwargs):
        super(AdminCategoriesProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['slug'].widget.attrs['placeholder'] = 'Введите url'

        self.fields['description'].widget.attrs['placeholder'] = 'Полное описание категории'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class AdminOrderForm(forms.ModelForm):
    """Добавление двух полей в редактирование заказа в админке"""
    class Meta:
        model = Order
        fields = ('status', 'is_active')


