import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
api_key = "sJ3y4ptsRHDuMXVnMrwW"

HPI_data = pd.read_pickle('07_fiddy_states.pickle')

# add a column of mutiple
#HPI_data['TX2'] = HPI_data['TX'] * 2
#print(HPI_data[['TX','TX2']].head())

# plot the graph
#HPI_data.plot()
#plt.legend().remove()
#plt.show()


# get another set of data by percentage change and plot to graph
def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]

def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken=api_key)
        df.columns = [str(abbv)]
        print(query)
        # key to percentage
        # df = df.pct_change()
        # measure chaage compared to the start point instead of last year value
        df[abbv] = (df[abbv]-df[abbv][0]) / df[abbv][0] * 100.0
        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
            
    #pickle_out = open('08_fiddy_states2.pickle','wb')
    pickle_out = open('08_fiddy_states3.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

#grab_initial_state_data()

# display the grabbed result

HPI_data2 = pd.read_pickle('08_fiddy_states2.pickle')

#HPI_data2.plot()
#plt.legend().remove()
#plt.show()

#grab_initial_state_data()
HPI_data3 = pd.read_pickle('08_fiddy_states3.pickle')

#HPI_data3.plot()
#plt.legend().remove()
#plt.show()


# from youtube comment change frequently

col = "United States"
col = "Value"

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df[col] = (df[col]-df[col][0]) / df[col][0] * 100.0
    return df

#fig = plt.figure()
#ax1 = plt.subplot2grid((1,1), (0,0))

#HPI_data = pd.read_pickle('08_fiddy_states3.pickle')
#benchmark = HPI_Benchmark()
#HPI_data.plot(ax=ax1)
#benchmark.plot(color='k',ax=ax1, linewidth=10)

#plt.legend().remove()
#plt.show()


HPI_data = pd.read_pickle('08_fiddy_states3.pickle')
HPI_State_Correlation = HPI_data.corr()
#print(HPI_State_Correlation)
print(HPI_State_Correlation.describe())

