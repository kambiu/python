import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
api_key = "sJ3y4ptsRHDuMXVnMrwW"

col = "Value"

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df[col] = (df[col]-df[col][0]) / df[col][0] * 100.0
    return df

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

m30 = mortgage_30y()
HPI_data = pd.read_pickle('08_fiddy_states3.pickle')

HPI_bench = HPI_Benchmark()

state_HPI_M30 = HPI_data.join(m30)

print(state_HPI_M30.corr()['M30'].describe())
