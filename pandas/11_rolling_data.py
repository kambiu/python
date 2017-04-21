import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
api_key = "sJ3y4ptsRHDuMXVnMrwW"



fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
HPI_data = pd.read_pickle('08_fiddy_states3.pickle')

#HPI_data['TX12MA'] = pd.rolling_mean(HPI_data['TX'], 12) # moving average

#HPI_data['TX12STD'] = pd.rolling_std(HPI_data['TX'], 12)

#print(HPI_data[['TX','TX12MA', 'TX12STD']].head())

# HPI_data.dropna(inplace=True)

#HPI_data[['TX','TX12MA']].plot(ax=ax1)
#HPI_data[['TX12STD']].plot(ax=ax2)

TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)

HPI_data['TX'].plot(ax=ax1, label='TX HPI')
HPI_data['AK'].plot(ax=ax1, label='AK HPI')

ax1.legend(loc=4)

TX_AK_12corr.plot(ax=ax2, label='TX_AK_12corr')

plt.legend(loc=4)
plt.show()

