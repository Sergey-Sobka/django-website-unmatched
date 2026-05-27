from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create demo admin user for Render deploy.'

    def handle(self, *args, **options):
        User = get_user_model()

        user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@example.com',
                'role': User.Roles.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )

        user.email = 'user@example.com'
        user.role = User.Roles.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.set_password('user12345')
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS('Demo admin user was created.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Demo admin user already exists and was updated.')
            )
