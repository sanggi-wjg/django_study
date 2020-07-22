import json
from json.decoder import JSONDecodeError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from apps.stock.forms import FinanceInfoForm, PivotForm
from apps.stock.models import Items, Pivot
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.scrap.module.scrap_consensus import Scrap_Consensus
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
        data = Items.objects.select_related('stock_section_name_id', 'stock_section_multiple_id').values(
            'id', 'name', 'code', 'stock_section_multiple_id__multiple', 'stock_section_name_id__name'
        ).get(code = self.kwargs['code'])
        print(data)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Stock Detail'
        context['pivot'] = Pivot.objects.filter(stock_items_id = context[self.context_object_name].get('id')).order_by('-date')
        context['finance_info'] = MongoDB().find_list('finance_info', { "stock_items_code": self.kwargs['code'] })
        return context


class CreatePivotProc(LoginRequiredMixin, View):
    template_name = 'stock/create_pivot_popup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = {
            'view_title': 'Create Pivot',
            'stock_item': get_object_or_404(Items, code = self.kwargs.get('code')),
            'pivot_form': PivotForm(initial = { 'stock_items_id': stock_item.id }).as_p(),
        })

    def post(self, request, *args, **kwargs):
        pivot_form = PivotForm(request.POST)
        stock_item = get_object_or_404(Items, code = self.kwargs.get('code'))

        if pivot_form.is_valid():
            pivot = pivot_form.save(commit = False)
            pivot.stock_items_id = stock_item
            pivot.base_line = (pivot.prev_closing_price + pivot.prev_low_price + pivot.prev_high_price) / 3
            pivot.resist_line_1 = (pivot.base_line * 2) - pivot.prev_low_price
            pivot.resist_line_2 = pivot.base_line + (pivot.prev_high_price - pivot.prev_low_price)
            pivot.resist_line_3 = pivot.prev_high_price + (pivot.base_line - pivot.prev_low_price) * 2
            pivot.support_line_1 = (pivot.base_line * 2) - pivot.prev_high_price
            pivot.support_line_2 = pivot.base_line - (pivot.prev_high_price - pivot.prev_low_price)
            pivot.support_line_3 = pivot.prev_low_price - (pivot.prev_high_price - pivot.base_line) * 2
            pivot.recommend_high_price = (pivot.resist_line_1 + pivot.base_line) / 2
            pivot.recommend_low_price = (pivot.base_line + pivot.support_line_1) / 2
            pivot.save()

            return popup_close()

        else:
            return render(request, self.template_name, context = {
                'view_title': 'Create Pivot',
                'stock_item': stock_item,
                'pivot_form': PivotForm(initial = { 'stock_items_id': stock_item.id }).as_p(),
                'errors'    : pivot_form.errors,
            })


class FinanceInfo(LoginRequiredMixin, View):
    template_name = 'stock/create_finance_info_popup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = {
            'view_title'       : 'Create Finance Info',
            'finance_info_form': FinanceInfoForm().as_p()
        })

    def post(self, request, *args, **kwargs):
        code = self.kwargs.get('code')
        finance_info_form = FinanceInfoForm(request.POST)

        if finance_info_form.is_valid():
            mongo = MongoDB()
            mongo.create('finance_info', {
                'stock_items_code': code,
                'year'            : finance_info_form.cleaned_data['year'],
                'total_sales'     : finance_info_form.cleaned_data['total_sales'],
                'business_profit' : finance_info_form.cleaned_data['business_profit'],
            })
            mongo.close()
            return popup_close()

        else:
            return render(request, self.template_name, context = {
                'view_title'       : 'Create Finance Info',
                'finance_info_form': FinanceInfoForm().as_p(),
                'errors'           : finance_info_form.errors
            })

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            code = self.kwargs.get('code')
            year = data.get('year')
            if not code: raise ValueError('Empty code')
            if not year: raise ValueError('Empty year')

            mongo = MongoDB()
            result = mongo.remove('finance_info', { "stock_items_code": code, "year": int(year) })

        except Exception as e:
            if isinstance(e, (ValueError, JSONDecodeError)):
                return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': e.__str__() }))
            else:
                return HttpResponseServerError(json.dumps({ 'code': '2222', 'msg': e.__str__() }))
        else:
            return JsonResponse({
                'code': '0000'
            })


class ScrapFinancialInfo(LoginRequiredMixin, View):
    """
    재무정보 스크랩해서 갱신 하기
    """

    def post(self, request, *args, **kwargs):
        try:
            scrap = Scrap_Consensus()
            result = scrap.run('https://wisefn.finance.daum.net/company/c1010001.aspx?cmp_cd={stock_code}'.format(stock_code = '005930'))
            self.save_financial_data(result)

        except Exception as e:
            print_exception()
            return JsonResponse({ 'code': '1111', 'msg': 'failure' })

        return JsonResponse({ 'code': '0000', 'msg': 'success' })

    def save_financial_data(self, parse_data):
        for data in parse_data:
            fs = MongoDB().find_one('finance_info', { "stock_items_code": self.kwargs['code'], 'year': data['year'] })

            if not fs:
                MongoDB().create('finance_info', {
                    'stock_items_code': self.kwargs['code'],
                    'year'            : data['year'],
                    'total_sales'     : data['total_sales'],
                    'total_sales_yoy' : data['total_sales_yoy'],
                    'business_profit' : data['business_profit'],
                    'net_profit'      : data['net_profit'],
                    'eps'             : data['eps'],
                    'per'             : data['per'],
                    'pbr'             : data['pbr'],
                    'roe'             : data['roe'],
                    'evebitda'        : data['evebitda'],
                    'debt_ratio'      : data['debt_ratio'],
                    'epsroe'          : int(data['eps'] * data['roe'])
                })
