import matplotlib.pyplot as plt

from pandas import DataFrame
from typing import List

from apps.third_party.plot.plt_helpers import plt_path, plt_colors, financial_crisis_list

plt.rcParams["font.family"] = 'NanumGothic'
plt.rcParams["figure.figsize"] = (60, 20)
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['font.size'] = 30
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 2


# plt.rcParams['axes.grid.axis'] = 'both'
# plt.rcParams['axes.grid.which'] = 'major'


def show_plot_list(df_1: List[DataFrame], df_1_label: List[str], df_1_y_label: str,
                   df_2: List[DataFrame] = None, df_2_label: List[str] = None, df_2_y_label: str = None,
                   plot_format = None, filedir: str = None, filename: str = None
                   ):
    if len(df_1) != len(df_1_label):
        raise ValueError('DataFrame 1 Length Is Not Matched')
    if df_2 and df_2_label and len(df_2) != len(df_2_label):
        raise ValueError('DataFrame 2 Length Is Not Matched')

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if plot_format:
        locator, formatter = plot_format()
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(formatter)

    fc_list = financial_crisis_list()
    line_list = []
    no = 0

    ax1.set_ylabel(df_1_y_label)
    for df, label in zip(df_1, df_1_label):
        line = ax1.plot(df, color = plt_colors(no), label = df)
        line_list.append(line)
        no += 1

        index = df.index
        first, last = str(index[0]), str(index[-1])
        for fc in fc_list:
            if first <= fc[0] and fc[1] <= last:
                ax1.axvspan(fc[0], fc[1], color = 'gray', alpha = 0.2)

    if df_2 is not None:
        ax2 = ax1.twinx()
        ax2.set_ylabel(df_2_y_label)

        for df, label in zip(df_2, df_2_label):
            line = ax2.plot(df, color = plt_colors(no), label = label)
            line_list.append(line)
            no += 1

    lines = [x[0] for x in line_list]
    labels = df_1_label + df_2_label if df_2_label else df_1_label
    ax1.legend(lines, labels, loc = 'upper left')

    if filename is None or filedir is None:
        plt.show()
    else:
        path = plt_path(filedir, filename)
        plt.savefig(path, bbox_inches = 'tight', pad_inches = 0.5)

    plt.grid(True, which = 'both', axis = 'x', color = 'gray', alpha = 0.5, linestyle = '--')
    plt.close(fig)


def show_plot_twinx(df_1: DataFrame, df_1_label: str, df_2: DataFrame, df_2_label: str, plot_format = None, filedir: str = None, filename: str = None):
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
    # [<matplotlib.lines.Line2D object at 0x7f85e6c6cdf0>, <matplotlib.lines.Line2D object at 0x7f85e6c33400>]
    lns = line1 + line2
    labs = [x.get_label() for x in lns]
    ax1.legend(lns, labs, loc = 'upper left')

    if filename is None or filedir is None:
        plt.show()
    else:
        filepath = plt_path(filedir, filename)
        plt.savefig(filepath, bbox_inches = 'tight', pad_inches = 0.5)

    plt.close(fig)


def show_plot(df: DataFrame, df_label: str):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_ylabel(df_label)
    line1 = ax1.plot(df, color = 'blue', label = df_label)

    plt.show()
    plt.close(fig)
