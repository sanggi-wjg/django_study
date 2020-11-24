import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame

from apps.third_party.util.utils import validate_path
from sample.settings import MEDIA_ROOT


def plt_year_format():
    return mdates.YearLocator(), mdates.DateFormatter('%Y')


def plt_year_month_format():
    return mdates.MonthLocator(), mdates.DateFormatter('%Y-%M')


def plt_path(filename: str):
    path = os.path.join(MEDIA_ROOT, 'plt')
    validate_path(path)

    return os.path.join(path, filename)


def show_twinx_plot(df_1: DataFrame, df_1_label: str, df_2: DataFrame, df_2_label: str, plot_format = None, if_filename: str = None):
    plt.rcParams["figure.figsize"] = (60, 20)
    plt.rcParams['font.size'] = 20

    # fig, ax1 = plt.subplots()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if plot_format:
        locator, formatter = plot_format()
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)

    ax1.set_ylabel(df_1_label)
    line1 = ax1.plot(df_1, color = 'blue', label = df_1_label)

    ax2 = ax1.twinx()
    ax2.set_ylabel(df_2_label)
    line2 = ax2.plot(df_2, color = 'red', label = df_2_label)

    # ax1.legend(handles = (line1, line2), labels = (df_1_label, df_2_label), loc = 'upper right')
    lns = line1 + line2
    labs = [x.get_label() for x in lns]
    ax1.legend(lns, labs, loc = 'upper left')

    if if_filename is None:
        plt.show()
    else:
        plt.savefig(plt_path(if_filename), bbox_inches = 'tight', pad_inches = 0.5)

    plt.close(fig)
