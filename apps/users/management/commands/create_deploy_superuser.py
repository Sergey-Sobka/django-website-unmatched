import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create deploy superuser from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Deploy superuser was not created. '
                    'Set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD.'
                )
            )
            return

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': User.Roles.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )

        user.email = email
        user.role = User.Roles.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS('Deploy superuser was created.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Deploy superuser already exists and was updated.')
            )
