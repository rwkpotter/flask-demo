#!/usr/bin/env python
'''
create your own Flask app on Heroku that accepts a stock ticker input 
from the user and plots closing price data for the last month. 
The Quandle WIKI dataset provides this data for free, and you can use 
Python's Requests library along with simplejson to access it in Python via API. 
You can analyze the data using pandas and plot using Bokeh. By the end you should
 have some kind of interactive visualization viewable from the Internet
'''

from flask import Flask, render_template, request, redirect,flash,url_for, make_response

import requests
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

@app.route('/index',methods=['GET','POST'])
def index():
	#if request.method == 'GET':
	if request.method == 'POST':
		flash("Alright! That looks awesome!")
		#return render_template('index.html')
	else:
		return render_template('index.html')
		"""#request was a POST
		app.vars['ticker'] = request.form['ticker'].upper()
		app.vars['start_year'] = request.form['year']
		try: 
			int(app.vars['start_year'])
		#	app.vars['tag'] = 'Start year specified as %s' % app.vars['start_year']
		except ValueError: 
			app.vars['start_year'] = ''
			app.vars['tag'] = 'Start year not specified/recognized'
		app.vars['select'] = [feat[q] for q in range(3) if feat[q] in request.form.values()]
		return redirect('/graph')"""


@app.route('/graph',methods=['GET','POST'])
def graph():
	
	# Request data from Quandl and get into pandas
	# --------------------------------------------|
	'''req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
	req = '%s%s.json?&collapse=weekly' % (req,app.vars['ticker'])
'''
# Request data from Quandl and get into pandas
	# --------------------------------------------|
	#req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
	req = 'https://www.quandl.com/data/WIKI/'
	#api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % app_vars['ticker']
#try:
#    f = urlopen(api_url)
#except:
#    return render_template('error.html', ticker=app_vars['ticker'])
	req = '%s%s.json?&collapse=weekly' % (req,app.vars['ticker'])
	if not app.vars['start_year']=='':
		req = '%s&start_date=%s-01-01' % (req,app.vars['start_year'])
	r = requests.get(req)
	cols = r.json()['dataset']['column_names'][0:5]
	df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:,0:5],columns=cols)
	df.Date = pd.to_datetime(df.Date)
	df[['Open','High','Low','Close']] = df[['Open','High','Low','Close']].astype(float)
	if not app.vars['start_year']=='':
		if df.Date.iloc[-1].year>int(app.vars['start_year']):
			app.vars['tag'] = '%s, but Quandl record begins in %s' % (app.vars['tag'],df.Date.iloc[-1].year)
	app.vars['desc'] = r.json()['dataset']['name'].split(',')[0]
	
	
	# Make Bokeh plot and insert using components
	# ------------------- ------------------------|
	p = figure(plot_width=450, plot_height=450, title=app.vars['ticker'], x_axis_type="datetime")
	if 'Range' in app.vars['select']:
		tmpx = np.array([df.Date,df.Date[::-1]]).flatten()
		tmpy = np.array([df.High,df.Low[::-1]]).flatten()
		p.patch(tmpx, tmpy, alpha=0.3, color="gray",legend='Range (High/Low)')
	if 'Open' in app.vars['select']:
		p.line(df.Date, df.Open, line_width=2,legend='Opening price')
	if 'Close' in app.vars['select']:
		p.line(df.Date, df.Close, line_width=2, line_color="#FB8072",legend='Closing price')
	p.legend.orientation = "top_left"
		
	# axis labels
	p.xaxis.axis_label = "Date"
	p.xaxis.axis_label_text_font_style = 'bold'
	p.xaxis.axis_label_text_font_size = '16pt'
	p.xaxis.major_label_orientation = np.pi/4
	p.xaxis.major_label_text_font_size = '14pt'
	p.xaxis.bounds = (df.Date.iloc[-1],df.Date.iloc[0])
	p.yaxis.axis_label = "Price ($)"
	p.yaxis.axis_label_text_font_style = 'bold'
	p.yaxis.axis_label_text_font_size = '16pt'
	p.yaxis.major_label_text_font_size = '12pt'
	
	# render graph template
	# ------------------- ------------------------|
	script, div = components(p)
	return render_template('graph.html', bv=bv, ticker=app.vars['ticker'],
							ttag=app.vars['desc'], yrtag=app.vars['tag'],
							script=script, div=div)
		
	
@app.errorhandler(500)
def error_handler(e):
	return render_template('error.html',ticker=app.vars['ticker'],year=app.vars['start_year'])

#if __name__ == '__main__':
  #app.run(port=33507)
app.run(debug=-True, host = '0.0.0.0', port=8888)

#quandl.ApiConfig.api_key = '9UYdbeyqFgisovBywzub'


#Get Facebook's stock price in a pandas dataframe:
#data = quandl.get("WIKI/FB")

#Get monthly changes in Facebook's closing price for the year 2014:
#data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")

'''
okay, so if anyone doing the heroku project runs into the issue of their plots not rendering its because the heroku page is served over HTTPS so I fixed it by letting the browser decide so in my graph.html I had to omit the “http”

<link rel="stylesheet" href="//cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.css" type="text/css" />
   <script type="text/javascript" src="//cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.js"></script>
'''




