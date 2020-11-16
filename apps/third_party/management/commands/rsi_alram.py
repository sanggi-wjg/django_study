from django.core.management import BaseCommand

from apps.model.stock_price import StockPrice
from apps.model.stock_subs import StockSubs
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
        stock_list = StockSubs.objects.values('stocks_id__stock_name').all()

        for stock in stock_list:
            rsi = StockPrice.objects.current_rsi(stock['stocks_id__stock_name'])
            if rsi >= 60 or rsi <= 40:
                send_discord('[{}] RSI : {}'.format(stock['stocks_id__stock_name'], rsi))
