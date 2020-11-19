from django.http import JsonResponse

from apps.func.view_helpers import _name_replace
from apps.third_party.core.viewmixins import FuncViews, HttpViews
from apps.third_party.fdr.finance_data_image_etc_one import FinanceDataImageEtcOne


class FinancialMetrics(FuncViews):
    view_title = '재무지표'
    template_name = 'func/financial_metrics_popup.html'


class IndexSites(FuncViews):
    view_title = 'Index Site'
    template_name = 'func/index_site_list.html'


class IndexFinancialData(HttpViews):
    pass


class IndexFinancialDataImage(HttpViews):

    def get(self, request, *args, **kwargs):
        fd_type = _name_replace(self.kwargs['fd_type'])
        term = self.kwargs['term']

        fd = FinanceDataImageEtcOne(start_date = term, end_date = None)
        result_flag, image_path = fd.save_image(symbol = fd_type, media_path = fd_type)

        return JsonResponse({ 'msg': 'create' if result_flag else 'exist', 'image_path': image_path })


class InterestCalculator(FuncViews):
    view_title = '복리 계산기'
    template_name = 'func/interest_calc_popup.html'
