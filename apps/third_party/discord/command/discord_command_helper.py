import requests


async def is_users_order(user_message):
    if '!' in user_message[0]:
        return True

    return False


async def help_text():
    return '![주식종목명] : 가격 조회\n' \
           '!구독리스트 : 현재 구독 중인 종목\n' \
           '!구독 [주식종목명] : 구독하기'


async def current_stock_subscribe_list():
    response = requests.get(url = 'http://192.168.10.6:8000/discord/stock/subs/list')
    response = response.json()
    return response['content']


async def stock_subscribe(stock_name: str):
    response = requests.get(url = 'http://192.168.10.6:8000/discord/stock/subs/{}'.format(stock_name))
    response = response.json()
    return response['content']


async def stock_price(stock_name: str):
    response = requests.get(url = 'http://192.168.10.6:8000/discord/stock/price/{}'.format(stock_name))
    response = response.json()
    return response['content']
