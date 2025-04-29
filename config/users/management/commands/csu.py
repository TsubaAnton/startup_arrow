from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = 'ontontsuba@icloud.com'
        password = 'Onton1010'  # Замените на желаемый пароль

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_superuser(
                email=email,
                is_superuser=True,
                is_staff=True,
                country='Kyrgyzstan',  # Обязательное поле (укажите нужную страну)
                first_name='Admin',  # Необязательно, но лучше заполнить
                last_name='Adminov',  # Необязательно, но лучше заполнить
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
