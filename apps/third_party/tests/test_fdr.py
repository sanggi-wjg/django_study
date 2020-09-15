import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('GC', '2020-09-01')
df['Close'].plot()
print(df)

plt.rcParams["font.family"] = 'nanummyeongjo'
plt.rcParams["figure.figsize"] = (14, 4)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True
plt.show()
