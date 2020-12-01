from apps.third_party.plot.plt_utils import show_plot_list
from apps.third_party.util.dataframe_helper import set_dataframe


class ReportsCreator:

    def __init__(self):
        self.start_year = 1980
        self.end_year = 2020
        self.term = 10

    def make(self, target_list: list, filedir: str, standard: bool, normalization: bool):
        for year in range(self.start_year, self.end_year + 1, self.term):
            start_date, end_date = '{}-01-01'.format(year), '{}-12-31'.format(year + (self.term - 1))
            dataframe, dataframe_label = [], []

            for target in target_list:
                dataframe_label.append(target[2])
                dataframe.append(
                    set_dataframe(
                        start_date, end_date, target[0], target[1],
                        standard = standard,
                        normalization = normalization
                    )
                )

            show_plot_list(
                dataframe, dataframe_label, 'Number',
                filedir = filedir, filename = '{}_{}'.format(year, '_'.join(dataframe_label))
            )
