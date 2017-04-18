import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
api_key = "sJ3y4ptsRHDuMXVnMrwW"



fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))
HPI_data = pd.read_pickle('08_fiddy_states3.pickle')


# from utube comment --> .resample('A').mean()
#TX1yr = HPI_data['TX'].resample('A', how='ohlc').mean()
TX1yr = HPI_data['TX'].resample('A').ohlc()
print(TX1yr.head())

HPI_data['TX'].plot(ax=ax1, label='Monthly TX HPI')
TX1yr.plot(ax=ax1)

plt.legend(loc=4)
plt.show()
