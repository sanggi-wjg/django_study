import json
from datetime import datetime
from json.decoder import JSONDecodeError

from bson.json_util import dumps
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from apps.in_queue.vos import InQueue
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.colorful import print_red, print_yellow


@method_decorator(csrf_exempt, name = 'dispatch')
class InQueue(View):
    content_type = 'application/json'
    permitted_methods = ['get', 'post']

    ###############################################################################
    # GET
    ###############################################################################
    def get(self, request, *args, **kwargs):
        mongo = MongoDB()
        try:
            query_result = mongo.find_list('in_queue', query = { })
            query_result = dumps(query_result)
            print_yellow(query_result)

        except Exception as e:
            print_red(e.__class__, e.__str__())
            return HttpResponseBadRequest(json.dumps({ 'code': '1111' }), content_type = self.content_type)

        finally:
            mongo.close()

        return JsonResponse({ 'code': '0000', 'datalist': query_result }, content_type = self.content_type)

    ###############################################################################

    ###############################################################################
    # POST
    ###############################################################################
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

    def post(self, request, *args, **kwargs):
        mongo = MongoDB()
        try:
            datalist = self._get_datalist(request.POST.get('data'))
            queues = self._setup_in_queue(datalist)
            mongo.create_bulk('in_queue', [q.__dict__ for q in queues])

        except Exception as e:
            print_red(e.__class__, e.__str__())

            if isinstance(e, (ValueError, JSONDecodeError,)):
                return HttpResponseBadRequest(json.dumps({ 'code': '1111' }), content_type = self.content_type)
            else:
                return HttpResponseServerError(json.dumps({ 'code': '2222' }), content_type = self.content_type)
        finally:
            mongo.close()

        return JsonResponse({ 'code': '0000' }, content_type = self.content_type)

    ###############################################################################

    def put(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)

    def patch(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)

    def delete(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)
