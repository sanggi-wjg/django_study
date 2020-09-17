import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from matplotlib import font_manager

stock_list = [
    ["삼성전자", "005930"], ["SK하이닉스", "000660"], ["현대차", "005380"], ["셀트리온", "068270"],
    ["LG화학", "051910"], ["POSCO", "005490"], ["삼성물산", "028260"], ["NAVER", "035420"],
]
df_list = [fdr.DataReader(stock_code, '2020-09-01')['Close'] for stock_name, stock_code in stock_list]
df = pd.concat(df_list, axis = 1)
df.columns = [stock_name for stock_name, stock_code in stock_list]
print(df)
df.plot()

font_prop = font_manager.FontProperties(fname = '/usr/share/fonts/NanumFont/NanumGothic.ttf')

plt.rcParams["font.family"] = 'NanumGothic'
plt.rcParams["figure.figsize"] = (14, 4)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True
plt.title('한글')
plt.show()
