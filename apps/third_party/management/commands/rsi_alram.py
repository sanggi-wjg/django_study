import pandas as pd

from django.core.management import BaseCommand

from apps.model.stock_price import StockPrice
from apps.model.stock_subs import StockSubs
from apps.model.stocks import Stocks
from apps.third_party.discord.discord_hook import send_discord
from apps.third_party.util.utils import today_dateformat


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
        message = ''
        stock_list = StockSubs.objects.values('stocks_id__stock_name').all()

        for stock in stock_list:
            stock_name = stock['stocks_id__stock_name']
            RSI = StockPrice.objects.current_rsi(stock_name)

            if RSI >= 60 or RSI <= 40:
                try:
                    price = StockPrice.objects.values('open_price', 'close_price', 'low_price', 'high_price').get(
                        stocks_id = Stocks.objects.get(stock_name = stock_name).id,
                        date = today_dateformat(time_format = '%Y-%m-%d')
                    )
                    message += '[{}] 시가: {} / 고가: {} / 저가: {} / 현재: {} /  RSI : {}\n'.format(stock['stocks_id__stock_name'], price['open_price'], price['high_price'], price['low_price'], price['close_price'], RSI)

                except StockPrice.DoesNotExist:
                    pass

        send_discord(message)
