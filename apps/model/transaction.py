from django.db import transaction

from apps.model.portfolios import Portfolios
from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.util.utils import today_dateformat


# @transaction.atomic
# def transaction_example():
#     pass

def transaction_purchase_stock(portfolio_id: int, purchase_count: int, purchase_date: str, stock_code: str):
    # 해당날짜 가격 * 매입 수량
    purchase_price = StockPrice.objects.get(stocks_id = Stocks.objects.get(stock_code = stock_code).id, date = purchase_date).close_price
    purchase_price = purchase_price * purchase_count

    # 남은 예수금으로 구매할 수 있는지 체크
    portfolio = Portfolios.objects.get(id = portfolio_id)
    if (portfolio.portfolio_deposit - portfolio.portfolio_purchase_price) < purchase_price:
        raise Exception('구매금액이 예수금을 초과합니다.')

    with transaction.atomic():
        # 구매 정보 입력
        PortfoliosDetail.objects.purchase(purchase_date, purchase_count, portfolio_id, stock_code)

        # 사용금액 업데이트
        Portfolios.objects.filter(
            id = portfolio_id
        ).update(
            portfolio_purchase_price = portfolio.portfolio_purchase_price + purchase_price,
            update_date = today_dateformat(time_format = '%Y-%m-%d')
        )

    return True


def transaction_sell_stock():
    pass
