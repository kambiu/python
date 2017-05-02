import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean

style.use('fivethirtyeight')
api_key = "sJ3y4ptsRHDuMXVnMrwW"



def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    return mean(values)

housing_data = pd.read_pickle('14_HPI.pickle')
housing_data = housing_data.pct_change()

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)

print(housing_data.head())

#US = "United States"
US = "Value"

housing_data['US_HPI_future'] = housing_data[US].shift(-1)
housing_data.dropna(inplace=True)
print(housing_data[['US_HPI_future', US]].head())

housing_data['label'] = list(map(create_labels,housing_data[US], housing_data['US_HPI_future']))

print(housing_data.head())

housing_data['ma_apply_example'] = housing_data['M30'].rolling(window=10, center=False).apply(moving_average)

print(housing_data.tail())
