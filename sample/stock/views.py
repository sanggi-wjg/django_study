from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import PivotForm
from .models import Items
from .mongo_db import MongoDB


class StockItemList(LoginRequiredMixin, ListView):
    model = Items
    paginate_by = 10
    template_name = 'stock/stock_item_list.html'
    context_object_name = 'stock_items'
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
        context['finance_info'] = MongoDB().find_one('finance_info', { "stock_items_code": self.kwargs['code'] })

        return context


# class CreatePivot(LoginRequiredMixin, DetailView):
#     template_name = 'stock/create_pivot.html'
#     context_object_name = 'stock_item'
#
#     def get_object(self, queryset = None):
#         return get_object_or_404(Items, code = self.kwargs['code'])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['view_title'] = 'Create Pivot'
#         context['pivot_form'] = PivotForm(initial = { 'stock_items_id': context[self.context_object_name].id }).as_ul()
#
#         return context


class CreatePivotProc(LoginRequiredMixin, View):
    template_name = 'stock/create_pivot.html'

    def _get_stock_item(self, code: str):
        return get_object_or_404(Items, code = code)

    def _get_pivot_form(self, stock_item_id: int):
        return PivotForm(initial = { 'stock_items_id': stock_item_id }).as_ul()

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
            pivot.resist_line_2 = pivot.base_line + pivot.prev_high_price - pivot.prev_low_price
            pivot.resist_line_3 = pivot.prev_high_price + (pivot.base_line - pivot.prev_low_price) * 2
            pivot.support_line_1 = (pivot.base_line * 2) - pivot.prev_high_price
            pivot.support_line_2 = pivot.base_line - pivot.prev_high_price - pivot.prev_low_price
            pivot.support_line_3 = pivot.prev_low_price - (pivot.prev_high_price - pivot.base_line) * 2
            pivot.save()

            return popup_close()

        else:
            return render(request, self.template_name, context = {
                'view_title': 'Create Pivot',
                'stock_item': stock_item,
                'pivot_form': self._get_pivot_form(stock_item.id),
                'errors'    : pivot_form.errors,
            })


def popup_close():
    return HttpResponse('<script type="text/javascript">window.close()</script>')
