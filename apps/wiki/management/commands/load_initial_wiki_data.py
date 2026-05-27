from django.core.management import BaseCommand, call_command

from apps.wiki.models import GameSet


class Command(BaseCommand):
    help = 'Load initial wiki data only when the wiki database is empty.'

    def handle(self, *args, **options):
        if GameSet.objects.exists():
            self.stdout.write(
                self.style.WARNING('Wiki data already exists. Fixture was not loaded.')
            )
            return

        call_command('loaddata', 'fixtures/wiki_initial_data.json')

        self.stdout.write(
            self.style.SUCCESS('Initial wiki data was loaded.')
        )
