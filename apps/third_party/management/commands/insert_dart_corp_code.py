from apps.model.dart_corp_code import DartCorpCode
from django.core.management import BaseCommand

from apps.third_party.dart.dart_corp_code import get_corp_code_list


class Command(BaseCommand):
    help = 'Dart CorpCode'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        corp_list = get_corp_code_list()

        for d in corp_list:
            DartCorpCode.objects.register(
                corp_code = d['corp_code'],
                corp_name = d['corp_name'],
                stock_code = d['stock_code']
            )
