# Stockticker app

App to display the August 2016 closing price of a chosen company via its stock ticker symbol. An error is displayed if the user inputs an incorrect ticker symbol.

## index.html
Main page for the user to input the chosen company's stock ticker. 

## graph.html
Displays company name and graph of August 2016 data. A "choose another company"
link sends the user back to the main page.

## app.py
Python code to: read ticker symbol from the POST data; make a http request to the Quandl API; retrieve data in json format; convert json formatted data to a pandas dataframe object; construct graphical plot using Bokeh interactive visualization library; send constructed plot to graph.html template.
