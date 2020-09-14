import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('USD/KRW', '2010-01-01')
df.plot()
plt.show()
