import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame


def plt_year_format():
    return mdates.YearLocator(), mdates.DateFormatter('%Y')


def show_twinx_plot(df_1: DataFrame, df_1_label: str, df_2: DataFrame, df_2_label: str, show_year_format = False):
    plt.rcParams["figure.figsize"] = (60, 20)
    plt.rcParams['font.size'] = 20

    fig, ax1 = plt.subplots()
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax1.set_ylabel(df_1_label)
    ax1.plot(df_1, color = 'blue', label = df_1_label)
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.set_ylabel(df_2_label)
    ax2.plot(df_2, color = 'red', label = df_2_label)
    ax2.legend()

    plt.show()
    plt.close(fig)
