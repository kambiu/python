import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates



def bytedate2num(fmt):
    def converter(b):
        return mdates.strpdate2num(fmt)(b.decode('ascii'))
    return converter

date_converter = bytedate2num('%Y%m%d')

def graph_data(stock):

    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10y/csv'

    source_code = urllib.request.urlopen(stock_price_url).read().decode()

    stock_data = []
    split_source = source_code.split('\n')

    for line in split_source:
        split_line = line.split(',')
        if len(split_line) == 6:
            if 'values' not in line:
                stock_data.append(line)
    date, closep, highp, lowp, openp, volume = np.loadtxt(
        stock_data,
        delimiter=',',
	unpack=True,
	# %Y = full year. 2015
	# %y = partial year 15
	# %m = number month
	# %d = number day
	# %H = hours
	# %M = minutes
	# %S = seconds
	# 12-06-2014
	# %m-%d-%Y
	converters={0: date_converter}
    )


graph_data('TSLA')


