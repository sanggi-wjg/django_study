import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.model.pivot import Pivot
from apps.model.sectors import Sectors
from apps.model.stocks import Stocks
from apps.stock.forms import PivotForm
from apps.stock.view_helpers import stock_detail_get_context
from apps.third_party.database.collections.demand import demand_info_register
from apps.third_party.database.collections.financial_info import financial_info_register
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus
from apps.third_party.scrap.module.scrap_demand import Scrap_Demand
from apps.third_party.util.colorful import print_yellow
from apps.third_party.util.helpers import popup_close
from apps.third_party.util.exceptions import print_exception
from apps.third_party.core.viewmixins import ListViews, DetailViews, HttpViews


class StockList(ListViews):
    model = Stocks
    paginate_by = 50
    block_size = 10
    template_name = 'stock/stock_list.html'
    context_object_name = 'stock_list'
    ordering = ['id']
    extra_context = {
        'view_title': '기업 리스트'
    }


class StockDetail(DetailViews):
    template_name = 'stock/stock_detail.html'
    context_object_name = 'stock'

    def get_object(self, queryset = None):
        return Stocks.objects.get_detail_join_one(stock_code = self.kwargs['stock_code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].get('stock_name')
        context['pivot'] = Pivot.objects.filter(stocks_id = context[self.context_object_name].get('id')).order_by('-date')
        context.update(stock_detail_get_context(self.kwargs['stock_code']))
        return context


class SearchStockNSectorList(HttpViews):
    """
    Search Stock And Sector autocomplete ajax in header
    """

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        stock_list = Stocks.objects.values('stock_code', 'stock_name').filter(stock_name__icontains = term)
        sector_list = Sectors.objects.values('id', 'sector_name').filter(sector_name__icontains = term)

        result = [{ 'code': stock['stock_code'], 'name': stock['stock_name'], 'category': '' } for stock in stock_list]
        [result.append({ 'code': str(sector['id']), 'name': sector['sector_name'], 'category': 'sector' }) for sector in sector_list]

        print_yellow(result)
        return HttpResponse(json.dumps(result))


class CreatePivotProc(HttpViews):
    template_name = 'stock/create_pivot_popup.html'

    def get(self, request, *args, **kwargs):
        stock_item = get_object_or_404(Stocks, stock_code = self.kwargs.get('code'))
        return render(request, self.template_name, context = {
            'view_title': 'Create Pivot',
            'stock_item': get_object_or_404(Stocks, stock_code = self.kwargs.get('code')),
            'pivot_form': PivotForm(initial = { 'stocks_id': stock_item.id }).as_p(),
        })

    def post(self, request, *args, **kwargs):
        pivot_form = PivotForm(request.POST)

        if pivot_form.is_valid():
            Pivot.objects.register(self.kwargs['code'], pivot_form)
            return popup_close()

        else:
            stock = get_object_or_404(Stocks, stock_code = self.kwargs['code'])

            return render(request, self.template_name, context = {
                'view_title': 'Create Pivot',
                'stock_item': stock,
                'pivot_form': PivotForm(initial = { 'stocks_id': stock.id }).as_p(),
                'errors'    : pivot_form.errors,
            })


class ScrapFinancialInfo(HttpViews):
    """
    재무정보 스크랩해서 갱신 하기
    """

    def post(self, request, *args, **kwargs):
        try:
            scrap = Scrap_Consensus()
            scrap_data = scrap.scrap('https://wisefn.finance.daum.net/company/c1010001.aspx?cmp_cd={stock_code}'.format(stock_code = self.kwargs['stock_code']))
            financial_info_register(stock_code, financial_data = scrap_data)

        except Exception as e:
            print_exception()
            return JsonResponse({ 'code': '1111', 'msg': 'failure' })

        return JsonResponse({ 'code': '0000', 'msg': 'success' })


class ScrapDemandInfo(HttpViews):
    """
    수급 정보
    """

    def post(self, request, *args, **kwargs):
        try:
            scrap = Scrap_Demand()
            scrap_data = scrap.scrap('https://finance.daum.net/quotes/A{stock_code}#influential_investors/home'.format(stock_code = self.kwargs['stock_code']))
            demand_info_register(self.kwargs['stock_code'], demand_data = scrap_data)

        except Exception as e:
            print_exception()
            return JsonResponse({ 'code': '1111', 'msg': 'failure' })

        return JsonResponse({ 'code': '0000', 'msg': 'success' })
