import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from apps.model.portfolios import Portfolios
from apps.model.portfolios_detail import PortfoliosDetail
from apps.model.stocks import Stocks
from apps.third_party.core.viewmixins import ListViews, HttpViews, DetailViews
from apps.third_party.util.colorful import print_yellow
from apps.third_party.util.helpers import alert


class PortfolioList(ListViews):
    model = Portfolios
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_list'
    ordering = ['id']
    extra_context = {
        'view_title': '포트폴리오 리스트'
    }


class PortfolioDetail(DetailViews):
    model = Portfolios
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'portfolio'
    pk_url_kwarg = 'portfolio_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].portfolio_name + ' 포트폴리오'
        return context


class CreatePortfolio(HttpViews):
    template_name = 'portfolio/portfolio_create.html'
    view_title = '포트폴리오 생성'
    content_type = 'text/html'
    status = 200

    def _render(self, errors = ''):
        return render(self.request, self.template_name, content_type = self.content_type, status = self.status, context = {
            'view_title': self.view_title,
            'errors'    : errors
        })

    def get(self, request, *args, **kwargs):
        return self._render()

    def post(self, request, *args, **kwargs):
        portfolio_name = self.request.POST.get('portfolio_name')
        portfolio_deposit = int(self.request.POST.get('portfolio_deposit').replace(',', ''))
        user_id = int(request.user.id)

        if Portfolios.objects.is_exist_portfolio_name(portfolio_name = portfolio_name):
            return self._render('포트폴리오 이름을 확인해주세요.')

        Portfolios.objects.register(portfolio_name, portfolio_deposit, user_id)

        return HttpResponseRedirect('/portfolios')


class StockSearchAutocomplete(HttpViews):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        stock_list = Stocks.objects.values('stock_code', 'stock_name').filter(stock_name__icontains = term)
        result = [{ 'code': stock['stock_code'], 'name': stock['stock_name'] } for stock in stock_list]

        return HttpResponse(json.dumps(result))


class PortfolioStockBuyNSell(HttpViews):

    def post(self, request, *args, **kwargs):
        portfolio_id = int(kwargs.get('portfolio_id'))
        stock_code = request.POST.get('stock_code')
        stock_name = request.POST.get('stock_name')
        purchase_count = int(request.POST.get('purchase_count'))
        purchase_date = request.POST.get('purchase_date')

        try:
            # 남은 예수금으로 구매할 수 있는지 체크

            # 구매 정보 입력
            PortfoliosDetail.objects.purchase(
                purchase_date = purchase_date, stock_count = purchase_count,
                portfolio_id = portfolio_id, stock_code = stock_code
            )
        except Exception as e:
            return alert(e.__str__())

        return HttpResponseRedirect('/portfolios/{}'.format(portfolio_id))

    def delete(self, request, *args, **kwargs):
        pass
