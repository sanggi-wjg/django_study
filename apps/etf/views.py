from apps.model.etfs import Etfs
from apps.third_party.core.viewmixins import ListViews


class EtfList(ListViews):
    model = Etfs
    paginate_by = 50
    block_size = 10
    template_name = 'etf/etf_list.html'
    context_object_name = 'etf_list'
    ordering = ['id']
    extra_context = {
        'view_title': 'ETF 리스트'
    }

    def get_queryset(self):
        return self.model.objects.values('etf_code', 'etf_name', 'company_id__company_name').order_by('company_id').all()
