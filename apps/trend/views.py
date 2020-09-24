from django.shortcuts import render

from apps.third_party.core.viewmixins import HttpViews
from apps.trend.view_helpers import investor_trend_get


class InvestorTrend(HttpViews):
    template_name = 'trend/trend_list.html'

    def get(self, request, *args, **kwargs):
        """
        market 1:Kospi / 2:Kosdaq
        """
        market = self.kwargs.get('market', '1')
        investor_trend_get(market)

        return render(request, self.template_name, context = {
            'view_title': '{} 투자자 동향'.format({ '1': 'KOSPI', '2': 'KOSDAQ' }.get(market)),
        })
