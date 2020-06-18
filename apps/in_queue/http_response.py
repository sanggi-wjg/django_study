import json
from json.decoder import JSONDecodeError

from bson.json_util import dumps
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse

from apps.third_party.util.exception import DBError


def http_response_failed(e, response_msg = None, content_type = 'application/json'):
    if isinstance(e, (ValueError, JSONDecodeError,)):
        return HttpResponseBadRequest(json.dumps({ 'code': '1111', 'msg': response_msg }), content_type = content_type)

    if isinstance(e, (DBError,)):
        return HttpResponseBadRequest(json.dumps({ 'code': '2222', 'msg': response_msg }), content_type = content_type)

    else:
        return HttpResponseServerError(json.dumps({ 'code': '3333', 'msg': response_msg }), content_type = content_type)


def http_response_success(response_data, content_type = 'application/json'):
    return HttpResponse(json.dumps(response_data), content_type = content_type)


def http_response_success_mongo(response_data, content_type = 'application/json'):
    return HttpResponse(dumps(response_data), content_type = content_type)
