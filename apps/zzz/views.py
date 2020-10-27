from django.shortcuts import render

from apps.third_party.core.viewmixins import HttpViews


class ZZZController(HttpViews):
    template_name = 'zzz/zzz_list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = { })
