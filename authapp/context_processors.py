
def user_status(request):
    """Выводит статус пользователя. Не используется"""
    user = request.user
    if user.is_authenticated:
        status = 'Пользователь авторизованн'
    else:
        status = 'Пользователь не авторизованн'
    return {'status': status}






