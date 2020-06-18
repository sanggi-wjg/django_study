import json

from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from apps.in_queue.http_response import HttpJsonResponse
from apps.third_party.database.collections.in_queue import Mongo_InQueue
from apps.third_party.util.colorful import print_red, print_green
from apps.third_party.util.exception import print_exception


@method_decorator(csrf_exempt, name = 'dispatch')
class InQueue(View):
    content_type = 'application/json'
    permitted_methods = ['get', 'post']

    ###############################################################################
    def get(self, request, *args, **kwargs):
        try:
            result = Mongo_InQueue().query('get_list')

        except Exception as e:
            print_red(e.__class__, e.__str__())
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success_mongo({ 'code': '0000', 'result': result })

    ###############################################################################

    ###############################################################################
    def post(self, request, *args, **kwargs):
        try:
            result = Mongo_InQueue().query('insert_list', data = request.POST.get('data'))

        except Exception as e:
            print_red(e.__class__, e.__str__())
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success_mongo({ 'code': '0000', 'result': result })

    ###############################################################################


@method_decorator(csrf_exempt, name = 'dispatch')
class InQueueOne(View):
    content_type = 'application/json'
    permitted_methods = ['get', 'delete']

    def get(self, request, *args, **kwargs):
        try:
            product = Mongo_InQueue().query('get_productCd_one', productCd = self.kwargs.get('productCd'))

        except Exception as e:
            print_exception()
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success_mongo({ 'code': '0000', 'result': product })

    ###############################################################################

    def put(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.permitted_methods)

    ###############################################################################

    def patch(self, request, *args, **kwargs):
        try:
            request_body = json.loads(request.body)

            result = Mongo_InQueue().query(
                'update_productCd_one',
                productCd = self.kwargs.get('productCd'),
                data = request_body
            )

        except Exception as e:
            print_exception()
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success({ 'code': '0000', 'result': result })

    ###############################################################################

    def delete(self, request, *args, **kwargs):
        try:
            delete_count = Mongo_InQueue().query('delete_productCd', productCd = self.kwargs.get('productCd'))

        except Exception as e:
            print_exception()
            return HttpJsonResponse.fail(e, e.__str__())

        return HttpJsonResponse.success({ 'code': '0000', 'result': delete_count })

    ###############################################################################
