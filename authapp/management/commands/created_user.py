from django.core.management.base import BaseCommand
from authapp.models import User


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        new_user = User(email='abracadabra@mail.ru', is_active=True)
        new_user.save()
        print('Пользователь добавлен')






