from apps.model.portfolios import Portfolios
from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.fdr.finance_data_stock_price import FinanceDataStockPrice
from apps.third_party.util.colorful import print_yellow, print_green


def portfolio_summary(portfolios: Portfolios) -> list:
    result = []

    for port in portfolios:
        summary_price = _portfolio_summary_prices(port.id, port.portfolio_deposit)

        result.append({
            'portfolio_id'            : port.id,
            'portfolio_name'          : port.portfolio_name,
            'portfolio_purchase_price': port.portfolio_purchase_price,
            'portfolio_deposit'       : port.portfolio_deposit,
            'register_date'           : port.register_date,
            'update_date'             : port.update_date,

            'total_price'             : port.portfolio_deposit + summary_price[0],
            'total_income_price'      : summary_price[0],
            'total_income_rate'       : summary_price[1],
        })

    return result


def _portfolio_summary_prices(portfolio_id: int, portfolio_deposit: int = None) -> tuple:
    total_income_price, total_income_rate = 0, 0.0
    portfolio_stock_list = PortfoliosDetail.objects.get_groups(portfolio_id)

    for stock in portfolio_stock_list:
        prices = get_stock_prices(stock['stocks_id'], stock['purchase_date'], stock['total_stock_count'])
        total_income_price += prices[2]

    if len(portfolio_stock_list) > 0 and portfolio_deposit is not None:
        total_income_rate = round(float(total_income_price / portfolio_deposit) * 100, 2)

    return total_income_price, total_income_rate


def get_stock_prices(stocks_id: int, purchase_date: str, total_stock_count) -> tuple:
    current_price = StockPrice.objects.values('close_price').filter(stocks_id = stocks_id).last()['close_price']
    purchase_price = StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = purchase_date)['close_price']
    income_price = int((current_price - purchase_price) * total_stock_count)
    income_rate = round(income_price / (current_price * total_stock_count) * 100, 2)

    return current_price, purchase_price, income_price, income_rate


def portfolio_detail_stock_list(portfolio_stock_list: PortfoliosDetail) -> list:
    result = []
    """
    <PortfoliosDetailQuerySet [{'sell_date': None, 'stocks_id__stock_name': '삼성전자', 'stocks_id': 860, 'total_stock_count': 2, 'purchase_date': datetime.date(2020, 10, 5)}, {'sell_date': None, 'stocks_id__stock_name': 'KT&G', 'stocks_id': 101, 'total_stock_count': 1, 'purchase_date': datetime.date(2020, 10, 7)}]>
    {'current': 59300, 'purchase': 58700}
    """
    for stock in portfolio_stock_list:
        stocks_id = stock['stocks_id']
        prices = get_stock_prices(stocks_id, stock['purchase_date'], stock['total_stock_count'])

        result.append({
            'sell_date'        : stock['sell_date'],
            'stock_name'       : stock['stocks_id__stock_name'],
            'stocks_id'        : stock['stocks_id'],
            'total_stock_count': stock['total_stock_count'],
            'purchase_date'    : stock['purchase_date'],
            'current_price'    : prices[0],
            'purchase_price'   : prices[1],
            'income_price'     : prices[2],
            'income_rate'      : prices[3],
        })

    return result


def validate_portfolio_stock_price(stock_code: str, stock_name: str):
    stocks_id = Stocks.objects.get(stock_code = stock_code).id

    if not StockPrice.objects.filter(stocks_id = stocks_id).exists():
        fd = FinanceDataStockPrice()
        fd.register(stocks_id, stock_code, stock_name = stock_name)
