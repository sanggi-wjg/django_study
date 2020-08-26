import json

import pymongo

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.stock.forms import PivotForm
from apps.stock.models import Items, Pivot
from apps.third_party.database.collections.demand import Mongo_Demand
from apps.third_party.database.collections.financial_info import Mongo_FI
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus
from apps.third_party.scrap.module.scrap_demand import Scrap_Demand
from apps.third_party.util.helpers import popup_close
from apps.third_party.util.exceptions import print_exception
from apps.third_party.core.viewmixins import ListViews, DetailViews, HttpViews


class StockItemList(ListViews):
    model = Items
    paginate_by = 20
    block_size = 10
    template_name = 'stock/stock_item_list.html'
    context_object_name = 'stock_items'
    ordering = ['stock_section_name_id']
    extra_context = {
        'view_title': '기업 리스트'
    }


class StockItemSearchCompanyList(HttpViews):
    """
    Search Company autocomplete ajax in header
    """

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        items = Items.objects.values('code', 'name').filter(name__icontains = term)

        result = []
        for item in items:
            result.append({ 'code': item['code'], 'name': item['name'] })

        return HttpResponse(json.dumps(result))


class StockItemDetail(DetailViews):
    template_name = 'stock/stock_item_detail.html'
    context_object_name = 'stock_item'

    def get_object(self, queryset = None):
        return Items.objects.get_detail_join_one(stock_code = self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].get('name')
        context['pivot'] = Pivot.objects.filter(stock_items_id = context[self.context_object_name].get('id')).order_by('-date')
        context['finance_info'] = MongoDB().find_list('finance_info', { "stock_items_code": self.kwargs['code'] }).sort('year')

        context['demand_info'] = MongoDB().find_list('demand_info', { "stock_items_code": self.kwargs['code'] }).sort('date', pymongo.DESCENDING)
        context['summary_demand_info'] = {
            self._get_sums(MongoDB().find_list('demand_info', { "stock_items_code": self.kwargs['code'] }).sort('date', pymongo.DESCENDING).limit(5)),
            self._get_sums(MongoDB().find_list('demand_info', { "stock_items_code": self.kwargs['code'] }).sort('date', pymongo.DESCENDING).limit(10)),
            self._get_sums(MongoDB().find_list('demand_info', { "stock_items_code": self.kwargs['code'] }).sort('date', pymongo.DESCENDING).limit(15)),
            self._get_sums(MongoDB().find_list('demand_info', { "stock_items_code": self.kwargs['code'] }).sort('date', pymongo.DESCENDING).limit(20)),
        }
        return context

    def _get_sums(self, data):
        foreign_sum, company_sum = 0, 0

        for d in data:
            foreign_sum += d.get('foreign_purchase_volume')
            company_sum += d.get('company_purchase_volume')

        return foreign_sum, company_sum


class CreatePivotProc(HttpViews):
    template_name = 'stock/create_pivot_popup.html'

    def get(self, request, *args, **kwargs):
        stock_item = get_object_or_404(Items, code = self.kwargs.get('code'))
        return render(request, self.template_name, context = {
            'view_title': 'Create Pivot',
            'stock_item': get_object_or_404(Items, code = self.kwargs.get('code')),
            'pivot_form': PivotForm(initial = { 'stock_items_id': stock_item.id }).as_p(),
        })

    def post(self, request, *args, **kwargs):
        pivot_form = PivotForm(request.POST)

        if pivot_form.is_valid():
            Pivot.objects.register(self.kwargs['code'], pivot_form)
            return popup_close()

        else:
            stock_item = get_object_or_404(Items, code = self.kwargs['code'])

            return render(request, self.template_name, context = {
                'view_title': 'Create Pivot',
                'stock_item': stock_item,
                'pivot_form': PivotForm(initial = { 'stock_items_id': stock_item.id }).as_p(),
                'errors'    : pivot_form.errors,
            })


class ScrapFinancialInfo(HttpViews):
    """
    재무정보 스크랩해서 갱신 하기
    """

    def post(self, request, *args, **kwargs):
        try:
            scrap = Scrap_Consensus()
            scrap_data = scrap.run('https://wisefn.finance.daum.net/company/c1010001.aspx?cmp_cd={stock_code}'.format(stock_code = self.kwargs['code']))
            Mongo_FI().query('register', stock_items_code = self.kwargs['code'], fi_data = scrap_data)

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
            scrap_data = scrap.run('https://finance.daum.net/quotes/A{stock_code}#influential_investors/home'.format(stock_code = self.kwargs['code']))
            Mongo_Demand().query('register', stock_items_code = self.kwargs['code'], demand_data = scrap_data)

        except Exception as e:
            print_exception()
            return JsonResponse({ 'code': '1111', 'msg': 'failure' })

        return JsonResponse({ 'code': '0000', 'msg': 'success' })
