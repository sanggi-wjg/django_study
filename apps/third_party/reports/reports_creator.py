from apps.third_party.plot.plt_utils import show_plot_list
from apps.third_party.util.colorful import print_green
from apps.third_party.util.dataframe_helper import set_dataframe


class ReportsCreator:

    def __init__(self, start_year: int = 1980, end_year: int = 2020, term: int = 10):
        self.start_year = start_year
        self.end_year = end_year
        self.term = term

    def make(self, target_list: list, filedir: str, standard: bool, normalization: bool):
        print_green('[{}~{}] {} will be created.\nSTANDARD : {} | NORMALIZATION :{}'.format(self.start_year, self.end_year, filedir, standard, normalization))

        for year in range(self.start_year, self.end_year + 1, self.term):
            print_green('[{}~{}] create success'.format(year, year + self.term))
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
