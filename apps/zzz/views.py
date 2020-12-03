from time import sleep

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from apps.third_party.core.viewmixins import HttpViews


class ZZZController(HttpViews):
    template_name = 'zzz/zzz_list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = { })


class SleepController(View):

    def get(self, request, *args, **kwargs):
        sleep_time = self.kwargs.get('sleep_time', 5)
        sleep(sleep_time)
        return JsonResponse({ 'msg': 'sleep_time:{}'.format(sleep_time) })
