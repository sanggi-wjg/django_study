def _name_replace(name):
    replace_list = {
        'USDKRW': 'USD/KRW'
    }
    result = replace_list.get(name, None)

    if result is None:
        return name
    else:
        return result
