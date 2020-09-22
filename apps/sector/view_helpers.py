from apps.model.stocks import Stocks
from apps.third_party.database.mongo_db import MongoDB


def sector_list_get_sector_group(sector_list):
    result = []

    for sector in sector_list:
        stock = Stocks.objects.values('stock_code', 'stock_name').filter(sectors_id = sector.id).order_by('id')

        result.append({
            'sector_id'  : sector.id,
            'sector_name': sector.sector_name,
            'stock_group': [(s['stock_code'], s['stock_name']) for s in stock]
        })

    return result


def sector_detail_get_finance_info(sector):
    finance_info, company_finance_info = { }, { }

    stock_items = Stocks.objects.filter(sectors_id = sector.id).order_by('id')
    for stock in stock_items:
        finance_info.setdefault(stock.stock_name, MongoDB().find_list('finance_info', { 'stock_items_code': stock.stock_code }).sort('year'))

    for company_name, info in finance_info.items():
        for i in info:
            if company_name not in company_finance_info:
                company_finance_info.setdefault(company_name, { })

            if i['year'] not in company_finance_info[company_name].keys():
                company_finance_info[company_name].setdefault(i['year'], [i])
            else:
                company_finance_info[company_name][i['year']].append(i)

    return company_finance_info
