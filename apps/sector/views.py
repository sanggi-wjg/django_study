from django.shortcuts import get_object_or_404

from apps.stock.models import Section_Name, Items
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.core.viewmixins import ListViews, DetailViews


class SectorList(ListViews):
    model = Section_Name
    paginate_by = 20
    block_size = 10
    template_name = 'sector/sector_list.html'
    context_object_name = 'sector_group'
    ordering = ['name']
    extra_context = {
        'view_title': '업종 리스트'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'sector_group': self._get_sector_group(context['object_list']) })
        return context

    def _get_sector_group(self, sector_list):
        result = []

        for n, sector in enumerate(sector_list):
            stock_items = Items.objects.values('code', 'name').filter(stock_section_name_id = sector.id).order_by('id')

            sector_group = {
                'sector_id'     : sector.id,
                'sector_name'   : sector.name,
                'stock_of_group': []
            }

            for stock in stock_items:
                sector_group['stock_of_group'].append((stock['code'], stock['name']))

            result.append(sector_group)

        return result


class SectorDetail(DetailViews):
    template_name = 'sector/sector_detail.html'
    context_object_name = 'sector'

    def get_object(self, queryset = None):
        return get_object_or_404(Section_Name, id = self.kwargs['sector_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = context[self.context_object_name].name
        context['finance_info'] = self._get_sector_finance_info()
        return context

    def _get_sector_finance_info(self):
        finance_info, company_finance_info = { }, { }
        context = super().get_context_data()

        stock_items = Items.objects.filter(stock_section_name_id = context[self.context_object_name].id).order_by('id')
        for stock in stock_items:
            finance_info.setdefault(stock.name, MongoDB().find_list('finance_info', { 'stock_items_code': stock.code }).sort('year'))

        for company_name, info in finance_info.items():
            for i in info:
                if company_name not in company_finance_info:
                    company_finance_info.setdefault(company_name, { })

                if i['year'] not in company_finance_info[company_name].keys():
                    company_finance_info[company_name].setdefault(i['year'], [i])
                else:
                    company_finance_info[company_name][i['year']].append(i)

        return company_finance_info
