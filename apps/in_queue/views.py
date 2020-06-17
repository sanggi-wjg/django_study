import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import View

from apps.in_queue.vos import InQueue
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.colorful import print_red, print_yellow


class InQueueList(LoginRequiredMixin, ListView):
    pass


@method_decorator(csrf_exempt, name = 'dispatch')
class InQueueProc(View):
    content_type = 'application/json'

    # def head(self):
    #     response = HttpResponse()
    #     response['Content-Type'] = 'application/json'
    #     return response

    def _get_datalist(self, data):
        if not data: raise ValueError('Empty data')
        result = json.loads(data)
        return result.get('datalist')

    def _setup_in_queue(self, datalist):
        queues = []

        for data in datalist:
            queue = InQueue()
            queue.packageCd = data.get('packageCd')
            queue.productCd = data.get('productCd')
            queue.productItemCd = data.get('productItemCd')
            queue.productName = data.get('productName')
            queue.productUnitPrice = float(data.get('productUnitPrice'))
            queue.inOrderCd = data.get('inOrderCd')
            queue.inOrderDate = datetime.strptime(data.get('inOrderDate'), '%Y-%m-%d %H:%M:%S')

            queues.append(queue)

        return queues

    def _create_queue(self, queues):
        mongo = MongoDB()
        mongo.create_bulk('in_queue', [q.__dict__ for q in queues])
        mongo.close()

    def post(self, request, *args, **kwargs):
        try:
            datalist = self._get_datalist(request.POST.get('data'))
            queues = self._setup_in_queue(datalist)
            self._create_queue(queues)

        except Exception as e:
            print_red(e.__class__, e.__str__())

            if isinstance(e, (ValueError, JSONDecodeError,)):
                return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': e.__str__() }), content_type = self.content_type)
            else:
                return HttpResponseServerError(json.dumps({ 'code': '2222', 'msg': e.__str__() }), content_type = self.content_type)

        else:
            return JsonResponse({ 'code': '0000' }, content_type = self.content_type)
