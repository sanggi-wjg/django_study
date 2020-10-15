from apps.model.portfolios import Portfolios
from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stock_price import StockPrice
from apps.model.stocks import Stocks
from apps.third_party.fdr.finance_data_stock_price import FinanceDataStockPrice
from apps.third_party.util.colorful import print_yellow


def portfolio_summary(portfolios: Portfolios) -> list:
    result = []

    for port in portfolios:
        total_current_price, *_ = _portfolio_summary_prices(port.id, port.portfolio_setup_deposit)
        total_portfolio_price = port.portfolio_deposit + total_current_price
        total_income_price = total_portfolio_price - port.portfolio_setup_deposit
        total_income_rate = round((total_income_price / port.portfolio_setup_deposit) * 100, 2)

        result.append({
            'portfolio_id'           : port.id,
            'portfolio_name'         : port.portfolio_name,
            'portfolio_deposit'      : port.portfolio_deposit,
            'portfolio_setup_deposit': port.portfolio_setup_deposit,
            'register_date'          : port.register_date,
            'update_date'            : port.update_date,

            'total_price'            : total_portfolio_price,
            'total_income_price'     : total_income_price,
            'total_income_rate'      : total_income_rate,
        })
        # print_yellow(result)

    return result


def _portfolio_summary_prices(portfolio_id: int, portfolio_setup_deposit: int = None) -> tuple:
    total_current_price, total_income_price, total_income_rate = 0, 0, 0.0
    portfolio_stock_list = PortfoliosDetail.objects.values(
        'stocks_id', 'sell_date', 'purchase_date', 'stock_count', 'sell_count', 'stocks_id__stock_name', 'stocks_id__stock_code'
    ).filter(portfolio_id = portfolio_id)

    for stock in portfolio_stock_list:
        current_price, purchase_price, income_price, income_rate, sell_price = get_stock_prices(stock['stocks_id'], stock['purchase_date'], stock['stock_count'], stock['sell_date'])
        total_current_price += current_price * stock['stock_count']
        total_income_price += income_price

    if len(portfolio_stock_list) > 0 and portfolio_setup_deposit is not None:
        total_income_rate = round(float(total_income_price / portfolio_setup_deposit) * 100, 2)

    return total_current_price, total_income_price, total_income_rate


def get_stock_prices(stocks_id: int, purchase_date: str, stock_count: int, sell_date: str) -> tuple:
    current_price = StockPrice.objects.values('close_price').order_by('-date').filter(stocks_id = stocks_id).first()['close_price']
    purchase_price = StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = purchase_date)['close_price']
    income_price = int((current_price - purchase_price) * stock_count)
    income_rate = 0.0
    if stock_count > 0:
        income_rate = round((current_price / purchase_price) * 10, 2)

    sell_price = 0
    if sell_date:
        sell_date_list = [date.strip() for date in sell_date.split('\n')]
        for item in sell_date_list:
            item_split = item.split('(')
            date, count = item_split[0], int(item_split[1].replace(')', ''))
            sell_price = sell_price + (StockPrice.objects.values('close_price').get(stocks_id = stocks_id, date = date)['close_price'] * count)

    return current_price, purchase_price, income_price, income_rate, sell_price


def portfolio_detail_stock_list(portfolio_id: int) -> list:
    portfolio_stock_list = PortfoliosDetail.objects.values(
        'stocks_id', 'sell_date', 'purchase_date', 'stock_count', 'sell_count', 'stocks_id__stock_name', 'stocks_id__stock_code'
    ).filter(portfolio_id = portfolio_id)

    result = []
    for stock in portfolio_stock_list:
        stocks_id = stock['stocks_id']
        current_price, purchase_price, income_price, income_rate, sell_price = get_stock_prices(stocks_id, stock['purchase_date'], stock['stock_count'], stock['sell_date'])

        result.append({
            'stock_code'    : stock['stocks_id__stock_code'],
            'stock_name'    : stock['stocks_id__stock_name'],
            'stocks_id'     : stock['stocks_id'],
            'stock_count'   : stock['stock_count'],
            'sell_count'    : stock['sell_count'],
            'total_count'   : stock['stock_count'] + stock['sell_count'],
            'purchase_date' : stock['purchase_date'],
            'sell_date'     : stock['sell_date'],

            'current_price' : current_price,
            'purchase_price': purchase_price,
            'income_price'  : income_price,
            'income_rate'   : income_rate,
            'sell_price'    : sell_price,
        })

    return result


def validate_portfolio_stock_price(stock_code: str, stock_name: str):
    stocks_id = Stocks.objects.get(stock_code = stock_code).id

    if not StockPrice.objects.filter(stocks_id = stocks_id).exists():
        fd = FinanceDataStockPrice()
        fd.register(stocks_id, stock_code, stock_name = stock_name)
