from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.model.sectors import Sectors
from apps.model.stocks import Stocks
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.core.viewmixins import ListViews, DetailViews, HttpViews
from apps.third_party.fdr.finance_data_image_stock_list import FinanceDataImageStockList
from apps.third_party.util.colorful import print_yellow


class SectorList(ListViews):
    model = Sectors
    paginate_by = 20
    block_size = 10
    template_name = 'sector/sector_list.html'
    context_object_name = 'sector_list'
    ordering = ['sector_name']
    extra_context = {
        'view_title': '업종 리스트'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'sector_group': self._get_sector_group(context['object_list']) })
        return context

    def _get_sector_group(self, sector_list):
        result = []

        for sector in sector_list:
            stock = Stocks.objects.values('stock_code', 'stock_name').filter(sectors_id = sector.id).order_by('id')

            sector_group = {
                'sector_id'  : sector.id,
                'sector_name': sector.sector_name,
                'stock_group': []
            }

            for s in stock:
                sector_group['stock_group'].append((s['stock_code'], s['stock_name']))

            result.append(sector_group)

        return result


class SectorDetail(DetailViews):
    template_name = 'sector/sector_detail.html'
    context_object_name = 'sector'

    def get_object(self, queryset = None):
        return get_object_or_404(Sectors, id = self.kwargs['sector_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].sector_name
        context['finance_info'] = self._get_sector_finance_info()
        return context

    def _get_sector_finance_info(self):
        finance_info, company_finance_info = { }, { }
        context = super().get_context_data()

        stock_items = Stocks.objects.filter(sectors_id = context[self.context_object_name].id).order_by('id')
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


class SectorFinancialDataComparedPriceImage(HttpViews):

    def get(self, request, *args, **kwargs):
        sector_id = self.kwargs['sector_id']
        term = self.kwargs['term']

        sector = Sectors.objects.values('id').filter(id = sector_id)
        if not sector:
            return JsonResponse({ 'msg': '{} is not sectors id'.format(sector_id) })

        fdl = FinanceDataImageStockList(start_date = term, end_date = None)
        result_flag, image_path = fdl.save_image(
            symbol = [[stock['name'], stock['code']] for stock in Stocks.objects.values('stock_code', 'stock_name').filter(sector_id__id = sector_id)],
            media_path = sector_id
        )

        return JsonResponse({ 'msg': 'create' if result_flag else 'exist', 'image_path': image_path })
