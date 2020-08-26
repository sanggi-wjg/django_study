import json
from json.decoder import JSONDecodeError

from bson.json_util import dumps
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse

from apps.third_party.util.exceptions import DBError


class HttpJsonResponse:

    @staticmethod
    def fail(e, response_msg, content_type = 'application/json'):
        if isinstance(e, (ValueError, JSONDecodeError,)):
            return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': response_msg }), content_type = content_type)

        elif isinstance(e, (DBError,)):
            return HttpResponseBadRequest(json.dumps({ 'code': '2222', 'msg': response_msg }), content_type = content_type)

        else:
            return HttpResponseServerError(json.dumps({ 'code': '3333', 'msg': response_msg }), content_type = content_type)

    @staticmethod
    def success(response_data, content_type = 'application/json', status_code = 200):
        return HttpResponse(json.dumps(response_data), content_type = content_type, status = status_code)

    @staticmethod
    def success_mongo(response_data, content_type = 'application/json', status_code = 200):
        return HttpResponse(dumps(response_data), content_type = content_type, status = status_code)
