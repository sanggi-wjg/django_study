import pytest

from keras import Sequential, optimizers
from keras.layers import Dense

from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks


@pytest.skip
@pytest.mark.django_db
def test_keras():
    price_list = StockPrice.objects.values('close_price').filter(stocks_id = Stocks.objects.get(stock_name = '삼성전자').id).order_by('date')
    TRAIN_PRICE = [p['close_price'] for p in price_list]
    TEST_PRICE = [p['close_price'] for p in price_list]

    model = Sequential()
    model.add(Dense(1, input_dim = 1, activation = 'linear'))

    sgd = optimizers.SGD(lr = 0.01)
    model.compile(optimizer = sgd, loss = 'mse', metrics = ['accuracy'])
    model.fit(TRAIN_PRICE, TEST_PRICE, batch_size = 1, epochs = 100, shuffle = False)

    print(TEST_PRICE)
