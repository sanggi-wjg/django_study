from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.third_party.util.colorful import print_yellow


def portfolio_detail_stock_list(portfolio_stock_list: PortfoliosDetail) -> list:
    result = []
    """
    <PortfoliosDetailQuerySet [{'sell_date': None, 'stocks_id__stock_name': '삼성전자', 'stocks_id': 860, 'total_stock_count': 2, 'purchase_date': datetime.date(2020, 10, 5)}, {'sell_date': None, 'stocks_id__stock_name': 'KT&G', 'stocks_id': 101, 'total_stock_count': 1, 'purchase_date': datetime.date(2020, 10, 7)}]>
    {'current': 59300, 'purchase': 58700}
    """
    for stock in portfolio_stock_list:
        stocks_id = stock['stocks_id']
        result.append({
            'sell_date'        : stock['sell_date'],
            'stock_name'       : stock['stocks_id__stock_name'],
            'stocks_id'        : stock['stocks_id'],
            'total_stock_count': stock['total_stock_count'],
            'purchase_date'    : stock['purchase_date'],
            'current_price'    : StockPrice.objects.values('close_price').filter(stocks_id = stocks_id).last()['close_price'],
            'purchase_price'   : StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = stock['purchase_date'])['close_price'],
        })

    return result
