from apps.third_party.util.viewmixins import FuncViews


class FinancialMetrics(FuncViews):
    view_title = '재무지표'
    template_name = 'func/financial_metrics_popup.html'


class IndexSites(FuncViews):
    view_title = 'Index Site'
    template_name = 'func/index_site_list.html'
