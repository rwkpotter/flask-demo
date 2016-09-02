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
import re
import numpy as np
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
bv = bokeh.__version__

app = Flask(__name__)
app.secret_key='gfiotgndip54906i43otgklbmff9ewrpijq;nwke9q-EQW0RGPFSDSa'


@app.route('/')
def main():
  return render_template('index.html')

@app.route('/graph',methods=['POST'])
def graph():
	ticker=request.form['ticker'].upper()
	
	#start dates fixed for August for now
	start_date='2016-08-01'
	end_date='2016-08-31'

	req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
	req = '%s%s.json?start_date=%s&end_date=%s&api_key=9UYdbeyqFgisovBywzub' % (req,ticker,start_date,end_date)
	
	
	r = requests.get(req)
	if "quandl_error" in r.json():
		flash("Please enter a valid ticker code")
		return (redirect(url_for('main')))
		
	cols = r.json()['dataset']['column_names'][0:5]
	
	#Print just company name.
	name= r.json()['dataset']['name']
	name = re.sub(r'\).*$', ")", name)
	
	#make a pandas dataframe
	df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:,0:5],columns=cols)
	df.Date = pd.to_datetime(df.Date)
	df[['Open','High','Low','Close']] = df[['Open','High','Low','Close']].astype(float)
	
	#make graph
	p = figure(plot_width=450, plot_height=450, title=ticker, x_axis_type="datetime")
	p.line(df.Date, df.Close, line_width=3, line_color="Turquoise",legend='Closing price')

	
	#axis labels
	p.xaxis.axis_label = "Date"
	p.xaxis.axis_label_text_font_style = 'bold'
	p.xaxis.axis_label_text_font_size = '16pt'
	p.yaxis.axis_label = "Closing Price ($)"
	p.yaxis.axis_label_text_font_style = 'bold'
	p.yaxis.axis_label_text_font_size = '16pt'
	
	
	script, div = components(p)
	return render_template('graph.html', bv=bv, ticker=ticker, script=script, div=div, name=name)


if __name__ == '__main__':
  app.run(debug = True, host='0.0.0.0', port=33507)
