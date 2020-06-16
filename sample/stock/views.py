import json
from json.decoder import JSONDecodeError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import PivotForm, FinanceInfoForm
from .models import Items, Pivot
from .mongo_db import MongoDB


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
        return get_object_or_404(Items, code = self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = 'Stock Detail'
        context['pivot'] = Pivot.objects.filter(stock_items_id = context[self.context_object_name].id).order_by('stock_items_id', '-date')
        context['finance_info'] = MongoDB().find_list('finance_info', { "stock_items_code": self.kwargs['code'] })

        return context


class CreatePivotProc(LoginRequiredMixin, View):
    template_name = 'stock/create_pivot_popup.html'

    def _get_stock_item(self, code: str):
        return get_object_or_404(Items, code = code)

    def _get_pivot_form(self, stock_item_id: int):
        return PivotForm(initial = { 'stock_items_id': stock_item_id }).as_p()

    def get(self, request, *args, **kwargs):
        code = self.kwargs.get('code')
        stock_item = self._get_stock_item(code)

        return render(request, self.template_name, context = {
            'view_title': 'Create Pivot',
            'stock_item': stock_item,
            'pivot_form': self._get_pivot_form(stock_item.id),
        })

    def post(self, request, *args, **kwargs):
        pivot_form = PivotForm(request.POST)
        stock_item = self._get_stock_item(self.kwargs.get('code'))

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
                'pivot_form': self._get_pivot_form(stock_item.id),
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
        print(self.kwargs)
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
            print(result)

        except Exception as e:
            if isinstance(e, (ValueError, JSONDecodeError)):
                return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': e.__str__() }))
            else:
                return HttpResponseServerError(json.dumps({ 'code': '2222', 'msg': e.__str__() }))
        else:
            return JsonResponse({
                'code': '0000'
            })


def popup_close():
    return HttpResponse('<script type="text/javascript">window.close()</script>')
