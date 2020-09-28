from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.model.portfolios import Portfolios
from apps.third_party.core.viewmixins import ListViews, HttpViews


class PortfolioList(ListViews):
    model = Portfolios
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_list'
    ordering = ['id']
    extra_context = {
        'view_title': '포트폴리오 리스트'
    }


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
