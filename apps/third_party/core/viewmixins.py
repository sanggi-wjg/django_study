from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View


class ListViews(LoginRequiredMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(ListViews, self).get_context_data()

        if self.paginate_by and hasattr(self, 'block_size'):
            start_index = int((context['page_obj'].number - 1) / self.block_size) * self.block_size
            end_index = min(start_index + self.block_size, len(context['paginator'].page_range))
            context['page_range'] = context['paginator'].page_range[start_index:end_index]

        return context


class DetailViews(LoginRequiredMixin, DetailView):
    pass


class HttpViews(LoginRequiredMixin, View):
    pass


class FuncViews(HttpViews):
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
