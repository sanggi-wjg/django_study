import FinanceDataReader as fdr
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = __name__ + '.png'
TARGET_DATE = '1980-01-01'
# TARGET_DATE = '2015-01-01'

plt.rcParams["figure.figsize"] = (50, 20)
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['font.size'] = 30


def test_df():
    df_kospi = fdr.DataReader('KS11', TARGET_DATE)
    df_kospi = df_kospi['Close']

    df_usdkrw = fdr.DataReader('USD/KRW', TARGET_DATE)
    df_usdkrw = df_usdkrw['Close']

    df = pd.merge(df_kospi, df_usdkrw, left_index = True, right_index = True, how = 'left')
    df.columns = ['KOSPI', 'USD/KRW']

    fig, ax1 = plt.subplots()
    ax1.set_ylabel('KOSPI')
    ax1.plot(df['KOSPI'], color = 'green', label = 'KOSPI')

    ax2 = ax1.twinx()
    ax2.set_ylabel('USD/KRW')
    ax2.plot(df['USD/KRW'], color = 'blue', label = 'USD_KRW')

    # plt.legend(('KOSPI', 'USD_KRW'), loc = 'upper right')
    # plt.legend(handles = (ax1, ax2), labels = ('KOSPI', 'USD/KRW'), loc = 'upper right')
    plt.savefig(FILE_NAME)
    plt.close(FILE_NAME)
