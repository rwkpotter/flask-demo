'''
create your own Flask app on Heroku that accepts a stock ticker input 
from the user and plots closing price data for the last month. 
The Quandle WIKI dataset provides this data for free, and you can use 
Python's Requests library along with simplejson to access it in Python via API. 
You can analyze the data using pandas and plot using Bokeh. By the end you should
 have some kind of interactive visualization viewable from the Internet
'''

from flask import Flask, render_template, request, redirect, flash, url_for, make_response

import requests
#import quandl
import numpy as np
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import show
from bokeh.charts import TimeSeries, output_file, show
from bokeh.embed import components
bv = bokeh.__version__

app = Flask(__name__)
app.secret_key='gfiotgndip54906i43otgklbmff9ewrpijq;nwke9q-EQW0RGPFSDSa'


@app.route('/')
def main():
  return render_template('index.html')

#@app.route('/message', methods=['POST'])
#def message():
#	if request.method=='POST': #if request.method == 'POST':
#		return request.form['ticker'].upper() #render_template('index.html')

@app.route('/graph',methods=['POST'])
def graph():
	ticker=request.form['ticker'].upper()
	
	start_date='2016-08-01'
	end_date='2016-08-31'

	req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
	req = '%s%s.json?start_date=%s&end_date=%s&api_key=9UYdbeyqFgisovBywzub' % (req,ticker,start_date,end_date)
	
	#quandl.ApiConfig.api_key = '9UYdbeyqFgisovBywzub'

	

	#data = quandl.get("WIKI/"+ticker, start_date=start_date, end_date=end_date, column_index=4)
	#df = pd.DataFrame(data)
	#df=df.rename(columns = {'one':'bob'}, inplace = True)
	
	r = requests.get(req)
	if "quandl_error" in r.json():
		flash("Please enter a valid ticker code")
		return (redirect(url_for('main')))
		
	cols = r.json()['dataset']['column_names'][0:5]
	df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:,0:5],columns=cols)
	df.Date = pd.to_datetime(df.Date)
	df[['Open','High','Low','Close']] = df[['Open','High','Low','Close']].astype(float)


	#return df.to_string()


	p = figure(plot_width=450, plot_height=450, title=ticker, x_axis_type="datetime")
	p.line(df.Date, df.Close, line_width=3, line_color="Turquoise",legend='Closing price')
	# #p = bokeh.charts.Line(data, x="", y="Close", color='firebrick')

	
	#axis labels
	p.xaxis.axis_label = "Date"
	p.xaxis.axis_label_text_font_style = 'bold'
	p.xaxis.axis_label_text_font_size = '16pt'
	p.yaxis.axis_label = "Closing Price ($)"
	p.yaxis.axis_label_text_font_style = 'bold'
	p.yaxis.axis_label_text_font_size = '16pt'
	
	
	# # render graph template
	# # ------------------- ------------------------|
	script, div = components(p)
	return render_template('graph.html', bv=bv, ticker=ticker, script=script, div=div)
	# return render_template ('graph.html', plot=p, script=script, div=div, data=data)


if __name__ == '__main__':
  app.run(debug = True, host='0.0.0.0', port=33507)


#quandl.ApiConfig.api_key = '9UYdbeyqFgisovBywzub'


#Get Facebook's stock price in a pandas dataframe:
#data = quandl.get("WIKI/FB")

#Get monthly changes in Facebook's closing price for the year 2014:
#data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")








