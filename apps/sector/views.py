from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.model.sectors import Sectors
from apps.model.stocks import Stocks
from apps.sector.view_helpers import sector_list_get_sector_group, sector_detail_get_finance_info
from apps.third_party.core.viewmixins import ListViews, DetailViews, HttpViews
from apps.third_party.fdr.finance_data_image_stock_list import FinanceDataImageStockList


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
        context.update({ 'sector_group': sector_list_get_sector_group(context['object_list']) })
        return context


class SectorDetail(DetailViews):
    model = Sectors
    template_name = 'sector/sector_detail.html'
    context_object_name = 'sector'
    pk_url_kwarg = 'sector_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].sector_name
        context['stock_list'] = Stocks.objects.filter(sectors_id = self.kwargs['sector_id']).order_by('id')
        context['finance_info'] = sector_detail_get_finance_info(context[self.context_object_name])
        return context


class SectorFinancialDataComparedPriceImage(HttpViews):

    def get(self, request, *args, **kwargs):
        sector_id = self.kwargs['sector_id']
        term = self.kwargs['term']

        sector = Sectors.objects.values('id').filter(id = sector_id)
        if not sector:
            return JsonResponse({ 'msg': '{} is not sectors id'.format(sector_id) })

        fdl = FinanceDataImageStockList(start_date = term, end_date = None)
        result_flag, image_path = fdl.save_image(
            symbol = [[s['stock_name'], s['stock_code']] for s in Stocks.objects.values('stock_code', 'stock_name').filter(sectors_id__id = sector_id)],
            media_path = sector_id
        )

        return JsonResponse({ 'msg': 'create' if result_flag else 'exist', 'image_path': image_path })
