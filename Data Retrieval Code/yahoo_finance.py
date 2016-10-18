import re
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import style
import requests
from dead_cat import *
import json 
import random
import csv


# Yahoo codes for ticker, change from 50d moving average, change from 52 week high, change from 52 week low, short ratio
codes = 'sm8k5j6s7'


# Read in the data (obtained in dead_cat.py) for the Dead Cat Bounce stocks into a dataframe  
# Calculate the short ratio which is defined as the Number of shares shorted/ Avg daily volume
final_DCB_df = pd.read_csv('FinalStats.csv', thousands=',')
final_DCB_df['Average_Volume'] = final_DCB_df['Average_Volume'].astype(float)
final_DCB_df['Shares_Short'] = final_DCB_df['Shares_Short'].astype(float)
final_DCB_df['Short_Ratio'] = final_DCB_df['Shares_Short']/final_DCB_df['Average_Volume']

final_DCB_df.drop(['Index','Average_Volume','Shares_Short'], axis=1, inplace=True)
final_DCB_df['Is_Dead_Cat'] = 1
cols = ['Ticker','Chg_from_Hi','Chg_from_Lo','Chg_from_50davg','Short_Ratio', 'Is_Dead_Cat']
final_DCB_df = final_DCB_df[cols]


# writes the final DCB df to a csv file.
def Consolidated_DCB_csv():
	DCB_Project_Data = open('DCB_ProjectData.csv','w')
	final_DCB_df.to_csv('DCB_ProjectData.csv')
	DCB_Project_Data.close()

Consolidated_DCB_csv()


# function that creates a string of tickers to pass as a parameter for the Yahoo finance call
def ticker_string_maker(array):
	global nonDCB_tickerstring
	nonDCB_tickerstring = ''
	for ticker in array:
		nonDCB_tickerstring += '+' + ticker 

	nonDCB_tickerstring = nonDCB_tickerstring[1:]


# Uses the requests module to get the data for each stock and then writes to a csv file
def write_stats_toCSV(tickerstr, csvfile, codes):
	r = requests.get('http://finance.yahoo.com/d/quotes.csv?s='+ tickerstr + '&' +'f=' + 'codes')
	csvfile.write(r.text)
	testing123.close()


# Transfer tickers from both files into a list
Allticker_list = []
file1 = open('nasdaqStocks.txt')
file2 = open('otherStocks.txt')
for line in file1.readlines()[1:] + file2.readlines()[1:]:
    stock = line.strip().split('|')[0]
    if (re.match(r'^[A-Z]+$',stock)):
        Allticker_list += [stock]

file1.close()
file2.close()

# From the list of 7832 tickers, pulls a random sample of 500 tickers
index_list = random.sample(range(7832), 500)
nonDCB_list = []
for index in index_list:
	if Allticker_list[index] not in final_DCBlist:	
		nonDCB_list.append(Allticker_list[index])


# Need to call these functions to store the data for non Dead Cat Bounce tickers.
"""ticker_string_maker(nonDCB_list)
YahooStats.csv = open('YahooStats.csv','a')
write_stats_toCSV(nonDCB_tickerstring, YahooStats, codes)"""


# Create a dataframe of Non DCB Stocks with the corresponding data and drop any NAN values
nonDCB_df = pd.read_csv('YahooStats.csv')
nonDCB_df.columns = ['Ticker','Chg_from_50davg','Chg_from_Hi','Chg_from_Lo', 'Short_Ratio']
nonDCB_df['Is_Dead_Cat'] = 0
nonDCB_df = nonDCB_df[cols]
nonDCB_df = nonDCB_df.dropna(how='any')
print nonDCB_df.count()

# Strip percent characters out of certain columns so we can convert to float
def strip_percents():
	cols_to_strip = ['Chg_from_50davg','Chg_from_Hi','Chg_from_Lo']
	for col in cols_to_strip:
		nonDCB_df[col] = nonDCB_df[col].apply(lambda x: x.strip("%"))
		nonDCB_df[col] = nonDCB_df[col].astype(float)

strip_percents()

# Create a final dataframe containing both DCB and non DCB data
Consolidated_Datadf = final_DCB_df.append(nonDCB_df, ignore_index=True)

# Create a final csv
Consolidated_data = open('CONSOLIDATED_DCB_DATA.csv','w')
Consolidated_Datadf.to_csv('CONSOLIDATED_DCB_DATA.csv')
Consolidated_data.close

