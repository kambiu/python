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

HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
print(HPI_data[['TX','TX1yr']].head())

#HPI_data.dropna(how='all', inplace=True) #2 how='all' only drop when tall # in dataset in Nan
#HPI_data.dropna(inplace=True) #2

#HPI_data.fillna(method='ffill', inplace=True) #3 take data from before
#HPI_data.fillna(method='bfill', inplace=True) #3 take data from future

#HPI_data.fillna(value=-9999, inplace=True) #4 fill with specific value
HPI_data.fillna(value=-9999, limit=10, inplace=True) #4 fill with specific value
print(HPI_data[['TX','TX1yr']].head())

HPI_data[['TX','TX1yr']].plot(ax=ax1)
print(HPI_data.isnull().values.sum()) #4
plt.legend(loc=4)
plt.show()

# To handle the missing data
# Option 1: Ignore  --> do nothing
# Option 2: Delete it
# Option 3: Predict it
# Option 4: Fill it with specific value
