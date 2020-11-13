from django.core.management import BaseCommand

from apps.model.stock_price import StockPrice
from apps.third_party.discord.discord_hook import send_discord


class Command(BaseCommand):
    help = 'test'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        https://www.macroption.com/rsi-calculation/

        * RSI Calculation Formula
            RSI = 100 – 100 / ( 1 + RS )
            RS = Relative Strength = AvgU / AvgD
            AvgU = average of all up moves in the last N price bars
            AvgD = average of all down moves in the last N price bars
            N = the period of RSI
            There are 3 different commonly used methods for the exact calculation of AvgU and AvgD (see details below)

        * RSI Calculation Step by Step
            Calculate up moves and down moves (get U and D)
            Average the up moves and down moves (get AvgU and AvgD)
            Calculate Relative Strength (get RS)
            Calculate the Relative Strength Index (get RSI)
        """
        rsi = StockPrice.objects.current_rsi('삼성전자')
        if rsi > 60:
            send_discord('삼성전자 RSI : {}'.format(rsi))
