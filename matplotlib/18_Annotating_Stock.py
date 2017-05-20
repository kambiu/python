import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

""" ch 15 """
# style.use('ggplot')
style.use('fivethirtyeight')
print(plt.style.available)

# to get the style sheet, location of styles sheets

#C:\Program Files\Python35\Lib\site-packages\matplotlib\mpl-data\stylelib

print(plt.__file__)

def bytespdate2num(fmt, encoding='utf-8'):
	strconverter = mdates.strpdate2num(fmt)
	def bytesconverter(b):
		s = b.decode(encoding)
		return strconverter(s)
	return bytesconverter



def graph_data(stock):


	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	
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
	
	#ax1.plot(date, closep)
	#ax1.plot(date, openp)
	
	for label in ax1.xaxis.get_ticklabels():
		label.set_rotation(45)

	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
	ax1.grid(True)
	
	""" ch 18 """
	# facecolor fc, edge color for ec, lw=line width
	bbox_props = dict(boxstyle='round',fc='w', ec='k',lw=1)

	ax1.annotate(str(closep[-1]), (date[-1], closep[-1]), xytext = (date[-1]+4, closep[-1]), bbox=bbox_props)
	##### annotation
	# ax1.annotate(
		# 'Bad News!',
		# (date[9],highp[9]),
		# xytext=(0.8, 0.9), # 80% of x-axis and 90% of y-axis
		# textcoords='axes fraction',
		# arrowprops = dict(facecolor='grey',color='grey') # try to move the graph and see what happen
	# )
	
	######placing text
	# font_dict = {
		# 'family':'serif',
		# 'color':'darkred',
		# 'size':15
	# }

	# ax1.text(date[10], closep[1],'eBay price', fontdict=font_dict)
	
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title(stock)
	#plt.legend()

	plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
	plt.show()


graph_data('ebay')


