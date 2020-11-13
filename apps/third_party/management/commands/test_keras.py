import numpy as np

from django.core.management import BaseCommand

from keras import Sequential, optimizers
from keras.layers import Dense, LSTM

from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.util.colorful import print_green, print_yellow


def make_datasets(datalist, dimension = 100):
    datasets = np.zeros((len(datalist), dimension))
    max_value = max(max(datalist))
    for i, seq in enumerate(datalist):
        datasets[i, seq] = seq / max_value
    return datasets


class Command(BaseCommand):
    help = 'test'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        price_list = StockPrice.objects.values('close_price').filter(stocks_id = Stocks.objects.get(stock_name = '삼성전자').id).order_by('date')
        price_list = [p['close_price'] for p in price_list]

        TRAIN_PRICE = np.array(price_list[0:100])
        TEST_PRICE = np.array(price_list[-100:])

        # model = Sequential()
        # model.add(LSTM(1000, return_sequences = True, input_shape = (1000, 1)))
        # model.add(LSTM(64, return_sequences = False))
        # model.add(Dense(1, input_dim = 1, activation = 'linear'))
        #
        # model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['accuracy'])
        # model.fit(TRAIN_PRICE, TEST_PRICE, batch_size = 16, epochs = 20, shuffle = False)
        #
        # predict = model.predict([1001])
        # print_yellow(predict)
