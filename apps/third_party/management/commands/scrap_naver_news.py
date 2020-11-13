from django.core.management import BaseCommand

from apps.third_party.naver.request_naver import RequestNaverNews


class Command(BaseCommand):
    help = 'Scrap Naver News'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # request_naver = RequestNaverNews()
        # request_naver.register_news('삼성전자')
        pass
