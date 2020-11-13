from django.http import JsonResponse
from django.views import View

from apps.model.stock_price import StockPrice
from apps.model.stock_subs import StockSubs
from apps.model.stocks import Stocks
from apps.third_party.util.exceptions import print_exception
from apps.third_party.util.utils import today_dateformat


class DiscordStockSubscribeList(View):

    def get(self, request, *args, **kwargs):
        try:
            datalist = StockSubs.objects.values('stocks_id__stock_name').all().order_by('stocks_id__stock_name')
            datalist = [p['stocks_id__stock_name'] for p in datalist]
            return JsonResponse({ 'content': '\n'.join(datalist) }, status = 200)

        except Exception:
            print_exception()
            return JsonResponse({ 'content': '띠용? 에러 발생' }, status = 400)


class DiscordStockSubscribe(View):

    def get(self, request, *args, **kwargs):
        try:
            StockSubs.objects.subscribe(kwargs.get('stock_name'))
            return JsonResponse({ 'content': 'success' }, status = 201)

        except Stocks.DoesNotExist:
            return JsonResponse({ 'content': '주식명을 확인해주세요.' }, status = 400)
        except Exception:
            print_exception()
            return JsonResponse({ 'content': '띠용? 에러 발생' }, status = 400)


class DiscordStockPrice(View):

    def get(self, request, *args, **kwargs):
        try:
            stock_price = StockPrice.objects.values('close_price', 'high_price', 'low_price').get(
                stocks_id = Stocks.objects.get(stock_name = kwargs.get('stock_name')).id,
                date = today_dateformat('%Y-%m-%d')
            )

            return JsonResponse({
                'content': '시가 : {}\n고가 : {}\n저가 : {}'.format(stock_price['close_price'], stock_price['high_price'], stock_price['low_price'])
            }, status = 200)

        except Stocks.DoesNotExist:
            return JsonResponse({ 'content': '주식명을 확인해주세요.' }, status = 400)
        except StockPrice.DoesNotExist:
            return JsonResponse({ 'content': '해당 주식은 현재 주가를 추적중이지 않습니다.' }, status = 400)
        except Exception:
            print_exception()
            return JsonResponse({ 'content': '띠용? 에러 발생' }, status = 400)
