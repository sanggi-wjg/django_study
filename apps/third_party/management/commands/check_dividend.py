from django.core.management import BaseCommand

from apps.third_party.dart.dart_dividend import sample_func


class Command(BaseCommand):
    help = 'Dart CorpCode'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sample_func()
