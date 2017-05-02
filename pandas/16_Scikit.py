import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm, preprocessing, cross_validation


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

X = np.array(housing_data.drop(['label','US_HPI_future'], 1))
X = preprocessing.scale(X)

y = y = np.array(housing_data['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)






