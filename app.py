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
import quandl
import numpy as np
import pandas as pd
import bokeh
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.embed import components
bv = bokeh.__version__

app = Flask(__name__)
app.secret_key='gfiotgndip54906i43otgklbmff9ewrpijq;nwke9q-EQW0RGPFSDSa'

app.vars={}
feat = ['Open','Close','Range']

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
	req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
	req = '%s%s.json?&collapse=weekly' % (req,ticker)
	
	quandl.ApiConfig.api_key = '9UYdbeyqFgisovBywzub'

	start_date='2016-08-01'
	end_date='2016-08-31'

	data = quandl.get("WIKI/FB.11", start_date=start_date, end_date=end_date)

	return data.to_string()
	# r = requests.get(req)
	# cols = r.json()['dataset']['column_names'][0:5]
	# df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:,0:5],columns=cols)
	# df.Date = pd.to_datetime(df.Date)
	# df[['Open','High','Low','Close']] = df[['Open','High','Low','Close']].astype(float)
	# if not app.vars['start_year']=='':
	# 	if df.Date.iloc[-1].year>int(app.vars['start_year']):
	# 		app.vars['tag'] = '%s, but Quandl record begins in %s' % (app.vars['tag'],df.Date.iloc[-1].year)
	# app.vars['desc'] = r.json()['dataset']['name'].split(',')[0]

	

	
#@app.route('/graph', methods=['GET','POST'])
#def graph:


if __name__ == '__main__':
  app.run(debug = True, host='0.0.0.0', port=33507)


#quandl.ApiConfig.api_key = '9UYdbeyqFgisovBywzub'


#Get Facebook's stock price in a pandas dataframe:
#data = quandl.get("WIKI/FB")

#Get monthly changes in Facebook's closing price for the year 2014:
#data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")








