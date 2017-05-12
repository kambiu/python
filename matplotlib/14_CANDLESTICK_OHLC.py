import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

"""
def bytedate2num(fmt):
	def converter(b):
		return mdates.strpdate2num(fmt)(b.decode('ascii'))
	return converter

date_converter = bytedate2num('%Y%m%d')


"""

def bytespdate2num(fmt, encoding='utf-8'):
	strconverter = mdates.strpdate2num(fmt)
	def bytesconverter(b):
		s = b.decode(encoding)
		return strconverter(s)
	return bytesconverter



def graph_data(stock):


	fig = plt.figure()
	"""1 subplot2grid"""
	#The 1,1 says this is a 1 x 1 grid.
	# Then 0,0 is us saying the "starting point" for this sub plot will be 0,0.
	# ** not plt.plot but ax1.plot 
	ax1 = plt.subplot2grid((1,1), (0,0))
	# compare to this one
	# ax1 = plt.subplot2grid((2,2), (0,1))
	
	stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1m/csv'

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
	converters={0: bytespdate2num("%Y%m%d")}
	)
	x = 0
	y = len(stock_data)
	ohlc = []
	while x < y:
		append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
		ohlc.append(append_me)
		x+=1
	candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
		
	for label in ax1.xaxis.get_ticklabels():
		label.set_rotation(45)

	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
	ax1.grid(True)
	
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title(stock)
	plt.legend()

	plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
	plt.show()


graph_data('twtr')


