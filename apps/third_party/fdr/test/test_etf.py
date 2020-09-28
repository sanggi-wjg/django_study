import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

dataframe = fdr.DataReader('069500', '2020-09-01')

dataframe['Close'].plot()
plt.show()
