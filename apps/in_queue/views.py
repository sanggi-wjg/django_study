import json
from datetime import datetime

from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from apps.in_queue.http_response import HttpJsonResponse
from apps.in_queue.vos import InQueue
from apps.third_party.database.mongo_dao import MongoDAO
from apps.third_party.database.mongo_db import MongoDB
from apps.third_party.util.colorful import print_red
from apps.third_party.util.exception import print_exception


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

        except Exception as e:
            print_red(e.__class__, e.__str__())
            return HttpJsonResponse.fail(e, e.__str__())

        finally:
            mongo.close()

        return HttpJsonResponse.success_mongo({ 'code': '0000', 'data': query_result })

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
            return HttpJsonResponse.fail(e, e.__str__())

        finally:
            mongo.close()

        return HttpJsonResponse.success({ 'code': '0000' })

        ###############################################################################


@method_decorator(csrf_exempt, name = 'dispatch')
class InQueueOne(View):
    content_type = 'application/json'
    permitted_methods = ['get', 'delete']

    def get(self, request, *args, **kwargs):
        try:
            product = MongoDAO().query('get_productCd_one', productCd = self.kwargs.get('productCd'))

        except Exception as e:
            print_exception()
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success_mongo({ 'code': '0000', 'data': product })

    ###############################################################################

    def put(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)

    ###############################################################################

    def patch(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)

    ###############################################################################

    def delete(self, request, *args, **kwargs):
        try:
            delete_count = MongoDAO().query('delete_productCd', productCd = self.kwargs.get('productCd'))

        except Exception as e:
            print_exception()
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success({ 'code': '0000', 'delete_count': delete_count })
