import pandas as pd
from pandas import DataFrame

from apps.model.index import Index
from apps.model.reports import Reports
from apps.third_party.reports.reader.reports_reader import ReportReaderData


def convert_dataframe(data, key: str):
    df = pd.DataFrame([x[key] for x in data], index = [x['date'] for x in data], columns = ['Number'])
    return df


def standard_normalization(dataframe: DataFrame, column: str):
    mean = dataframe.mean(axis = 0)
    std = dataframe.std(axis = 0)
    return (dataframe[column] - mean[column]) / std[column]


def set_dataframe(start_date: str, end_date: str, model_type: str, df_name: str, do_standard_normalization: bool = False):
    model_type = model_type.upper()

    if model_type == 'INDEX':
        dataframe = convert_dataframe(
            Index.objects.get_index_df(df_name, start_date, end_date),
            'number'
        )
        if do_standard_normalization:
            dataframe = standard_normalization(dataframe, 'Number')

    elif model_type == 'REPORT':
        name = ReportReaderData().data[df_name][0]
        dataframe = convert_dataframe(
            Reports.objects.get_report_df(name, start_date, end_date),
            'number'
        )
        if do_standard_normalization:
            dataframe = standard_normalization(dataframe, 'Number')

    else:
        raise ValueError('Invalid model_type')

    if not dataframe:
        raise ValueError('Nothing Has Set dataframe')

    return dataframe
