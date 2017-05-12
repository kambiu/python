import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import datetime as dt

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
	converters={0: bytespdate2num("%Y%m%d")}
	)

##	date, closep, highp, lowp, openp, volume = np.loadtxt(
##		stock_data,
##		delimiter=',',
##		unpack=True
##	)
##	
##	dateconv = np.vectorize(dt.datetime.fromtimestamp)
##	date = dateconv(date)

	
	#plt.plot_date(date, closep)

	ax1.plot_date(date, closep,'-', label='Price')

	# the labels (years) in x axis roate 45 degree
	for label in ax1.xaxis.get_ticklabels():
		label.set_rotation(45)

	#ax1.grid(True, color='b') # and also parameters
	ax1.grid(True)

	
	#ax1.xaxis.label.set_color('c')
	#ax1.yaxis.label.set_color('r')
	ax1.set_yticks([0,25,50,75]) # set yaxis values

	#ax1.fill_between(date, 0, closep, alpha=0.3) # fill colors
	ax1.fill_between(date, closep, closep[0], where=(closep > closep[0]), facecolor='g', alpha=0.3) # check with b4
	ax1.fill_between(date, closep, closep[0], where=(closep < closep[0]), facecolor='r', alpha=0.3) # check with b4
	# labels legends
	ax1.plot([],[],linewidth=5, label='loss', color='r',alpha=0.5)
	ax1.plot([],[],linewidth=5, label='gain', color='g',alpha=0.5)
	""" ch13 main points"""
	ax1.spines['left'].set_color('c')
	ax1.spines['right'].set_visible(False)
	ax1.spines['left'].set_visible(False)
	ax1.spines['left'].set_linewidth(5)
	ax1.tick_params(axis='x', colors='#f06215')
	ax1.axhline(closep[0], color='k', linewidth=5)
	""""""
	
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title(stock)
	plt.legend()

	plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
	plt.show()


graph_data('twtr')


