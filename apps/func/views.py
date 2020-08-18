from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View


class Views(LoginRequiredMixin, View):
    template_name = ''
    view_title = ''
    content_type = 'text/html'
    status = 200

    def get_context(self):
        return None

    def get(self, request, *args, **kwargs):
        if not self.template_name: raise NotImplementedError('PopupViews template_name is not declared')
        if not self.view_title: raise NotImplementedError('PopupViews view_title is not declared')

        context = { 'view_title': self.view_title }
        add_context = self.get_context()
        if add_context is not None:
            context.update(add_context)

        return render(request, self.template_name,
                      context = context,
                      content_type = self.content_type,
                      status = self.status)


class FinancialMetrics(Views):
    view_title = '재무지표'
    template_name = 'func/financial_metrics_popup.html'


class IndexSites(Views):
    view_title = 'Index Site'
    template_name = 'func/index_site_list.html'
