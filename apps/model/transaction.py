from django.db import transaction

from apps.model.portfolios import Portfolios
from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.util.colorful import print_yellow
from apps.third_party.util.exceptions import TransactionError
from apps.third_party.util.utils import today_dateformat


# @transaction.atomic
# def transaction_example():
#     pass

def transaction_purchase_stock(portfolio_id: int, purchase_count: int, purchase_date: str, stock_code: str):
    try:
        portfolio = Portfolios.objects.get(id = portfolio_id)
        # 해당날짜 가격 * 매입 수량
        purchase_price = StockPrice.objects.get(stocks_id = Stocks.objects.get(stock_code = stock_code).id, date = purchase_date).close_price * purchase_count
        # 남은 예수금으로 매입할 수 있는지 체크
        if portfolio.portfolio_deposit < purchase_price:
            raise TransactionError('매입금액이 예수금을 초과합니다.')

    except Portfolios.DoesNotExist:
        raise TransactionError('Invalid portfolio_id')
    except StockPrice.DoesNotExist:
        raise TransactionError('Price of stock is not saved')

    with transaction.atomic():
        # 구매 정보 입력
        PortfoliosDetail.objects.purchase(purchase_date, purchase_count, portfolio_id, stock_code)

        # 예수금 = 현재 예수금 - 매입금액
        Portfolios.objects.filter(id = portfolio_id).update(
            portfolio_deposit = portfolio.portfolio_deposit - purchase_price,
            update_date = today_dateformat(time_format = '%Y-%m-%d')
        )

    return True


def transaction_sell_stock(portfolio_id: int, sell_count: int, sell_date: str, purchase_date: str, stock_code: str):
    try:
        # 포트폴리오의 해당 종목 구매일자 정보 가져옴
        stocks_id = Stocks.objects.get(stock_code = stock_code).id
        portfolio = Portfolios.objects.get(id = portfolio_id)

        # 구매액, 판매액
        purchase_price = StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = purchase_date)['close_price']
        sell_price = StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = sell_date)['close_price']

        target_port = PortfoliosDetail.objects.values('purchase_date', 'stock_count', 'sell_count').get(
            portfolio_id = portfolio_id, purchase_date = purchase_date, stocks_id = stocks_id
        )

        # 매도일이 매입일 전이 아닌지 체크
        if target_port['stock_count'] < sell_count:
            raise TransactionError('매도수량이 매입수량을 초과합니다.')
        # 매도 수량이 가능한지 체크
        if target_port['purchase_date'].strftime('%Y-%m-%d') > sell_date:
            raise TransactionError('매도일이 매수일 보다 과거 입니다.')

    except Stocks.DoesNotExist:
        raise TransactionError('Invalid stock_code')
    except Portfolios.DoesNotExist:
        raise TransactionError('Invalid portfolio_id')
    except StockPrice.DoesNotExist:
        raise TransactionError('Price of stock is not saved')
    except PortfoliosDetail.DoesNotExist:
        raise TransactionError('Invalid portfolio_id, purchase_date, stocks_id')

    with transaction.atomic():
        # 포트폴리오 예수금 = 현재 예수금 + (매도금액 * 매도량)
        Portfolios.objects.filter(id = portfolio_id).update(
            portfolio_deposit = portfolio.portfolio_deposit + (sell_price * sell_count),
        )

        # 포트폴리오 종목 판매수량 업데이트
        # 포트폴리오 종목 매도일을 추가한 row 추가
        portfolio_detail = PortfoliosDetail.objects.get(portfolio_id = portfolio_id, purchase_date = purchase_date, stocks_id = stocks_id)
        PortfoliosDetail.objects.filter(portfolio_id = portfolio_id, purchase_date = purchase_date, stocks_id = stocks_id).update(
            stock_count = portfolio_detail.stock_count - sell_count,
            sell_count = portfolio_detail.sell_count + sell_count,
            sell_date = '{} {}({})'.format('{}\n'.format(portfolio_detail.sell_date) if portfolio_detail.sell_date is not None else '', sell_date, sell_count)
        )

    return True
