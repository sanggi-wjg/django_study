import json
from json.decoder import JSONDecodeError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from apps.stock.forms import PivotForm
from apps.stock.models import Items, Pivot
from apps.third_party.database.collections.demand import Mongo_Demand
from apps.third_party.database.collections.financial_info import Mongo_FI
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus
from apps.third_party.scrap.module.scrap_demand import Scrap_Demand
from apps.third_party.util.comm_helper import popup_close
from apps.third_party.util.exception import print_exception


class StockItemList(LoginRequiredMixin, ListView):
    model = Items
    paginate_by = 10
    template_name = 'stock/stock_item_list.html'
    context_object_name = 'stock_items'
    ordering = ['code']
    extra_context = {
        'view_title': 'Stock List'
    }


class StockItemDetail(LoginRequiredMixin, DetailView):
    template_name = 'stock/stock_item_detail.html'
    context_object_name = 'stock_item'

    def get_object(self, queryset = None):
        return Items.objects.get_detail_join_one(stock_code = self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Stock Detail'
        context['pivot'] = Pivot.objects.filter(stock_items_id = context[self.context_object_name].get('id')).order_by('-date')
        context['finance_info'] = MongoDB().find_list('finance_info', { "stock_items_code": self.kwargs['code'] })
        return context


class CreatePivotProc(LoginRequiredMixin, View):
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


class ScrapFinancialInfo(LoginRequiredMixin, View):
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


class ScrapDemandInfo(LoginRequiredMixin, View):
    """

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

# class FinanceInfo(LoginRequiredMixin, View):
#     template_name = 'stock/create_finance_info_popup.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, context = {
#             'view_title'       : 'Create Finance Info',
#             'finance_info_form': FinanceInfoForm().as_p()
#         })
#
#     def post(self, request, *args, **kwargs):
#         code = self.kwargs.get('code')
#         finance_info_form = FinanceInfoForm(request.POST)
#
#         if finance_info_form.is_valid():
#             mongo = MongoDB()
#             mongo.create('finance_info', {
#                 'stock_items_code': code,
#                 'year'            : finance_info_form.cleaned_data['year'],
#                 'total_sales'     : finance_info_form.cleaned_data['total_sales'],
#                 'business_profit' : finance_info_form.cleaned_data['business_profit'],
#             })
#             mongo.close()
#             return popup_close()
#
#         else:
#             return render(request, self.template_name, context = {
#                 'view_title'       : 'Create Finance Info',
#                 'finance_info_form': FinanceInfoForm().as_p(),
#                 'errors'           : finance_info_form.errors
#             })
#
#     def patch(self, request, *args, **kwargs):
#         pass
#
#     def delete(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)
#             code = self.kwargs.get('code')
#             year = data.get('year')
#             if not code: raise ValueError('Empty code')
#             if not year: raise ValueError('Empty year')
#
#             mongo = MongoDB()
#             result = mongo.remove('finance_info', { "stock_items_code": code, "year": int(year) })
#
#         except Exception as e:
#             if isinstance(e, (ValueError, JSONDecodeError)):
#                 return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': e.__str__() }))
#             else:
#                 return HttpResponseServerError(json.dumps({ 'code': '2222', 'msg': e.__str__() }))
#         else:
#             return JsonResponse({
#                 'code': '0000'
#             })
