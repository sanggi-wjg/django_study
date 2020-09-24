from apps.third_party.database.mongo_db import MongoDB


def investor_trend_get_data(market: str, from_date: str, to_date: str):
    trend_list = MongoDB().find_list('investor_trend', { 'market': market, "date": { "$gte": from_date, "$lte": to_date } }).sort('date')

    # ['개인', '외국인', '증권', '보험', '투신', '은행', '종금', '연기금', '사모펀드', '기타법인']
    labels, datasets = [], { 'personal': [], 'foreigner': [], 'invest_firm': [], 'insurance_firm': [], 'trust_firm': [], 'bank_firm': [], 'non_bank_firm': [], 'pension_fund': [], 'samo_fund': [], 'etf_firm': [] }

    for trend in trend_list:
        labels.append(trend['date'])
        datasets['personal'].append(trend['personal'])
        datasets['foreigner'].append(trend['foreigner'])
        datasets['invest_firm'].append(trend['invest_firm'])
        datasets['insurance_firm'].append(trend['insurance_firm'])
        datasets['trust_firm'].append(trend['trust_firm'])
        datasets['bank_firm'].append(trend['bank_firm'])
        datasets['non_bank_firm'].append(trend['non_bank_firm'])
        datasets['pension_fund'].append(trend['pension_fund'])
        datasets['samo_fund'].append(trend['samo_fund'])
        datasets['etf_firm'].append(trend['etf_firm'])

    return {
        'labels'  : labels,
        'datasets': datasets
    }
