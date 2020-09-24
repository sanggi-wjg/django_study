from apps.third_party.database.mongo_db import MongoDB


def investor_trend_get(market: str):
    result = MongoDB().find_list('investor_trend', { 'market': market }).sort('-date')

    # for r in result:
    #     print(r)
