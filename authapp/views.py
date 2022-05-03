from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from basketapp.models import Basket
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, ShopUserProfileEditForm
from authapp.models import User
from .utils import send_activate_mail


def verify(request, user_id, hash):
    """Активация ползователя по ссылке отправленной на почту и содержащей ключ активации"""
    try:
        user = get_object_or_404(User, pk=user_id)
        if user.activation_key == hash and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Активация пользователя {user} прошла успешно.')
            return HttpResponseRedirect(reverse('main:index'))

        raise Http404('Недействительная ссылка активации')
    except Exception as e:
        raise Http404


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    context = {'form': form, 'head': 'авторизация'}
    return render(request, 'authapp/login.html', context)


def register(request):
    """Регистрация пользователя и отправка ему письма для активации через функцию send_activate_mail"""
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_activate_mail(user)
            messages.success(request,
                             'Вы успешно зарегестрировались! Ссылка для активации профиля отправленна на почту.')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def profile(request, pk):
    """Профиль пользователя. Корзина отображается в профиле пользователя"""
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(data=request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            context = {'head': 'My_Shop - Профиль',
                       'form': form,
                       'profile_form': profile_form,
                       'baskets': Basket.objects.filter(user=request.user),
                       }
            return render(request, 'authapp/profile.html', context)
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {'head': ' My_Shop - Профиль',
               'form': form,
               'profile_form': profile_form,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'authapp/profile.html', context)
