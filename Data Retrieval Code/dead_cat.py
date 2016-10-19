import ticker_script
import re
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import style
import quandl
import requests
from sklearn import feature_selection, linear_model
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Read tickers of dead cat bounce stocks into a dataframe and drop all null values
DCB_df = pd.read_csv("dcb_tickers.csv", names=['EndDate', 'Ticker','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
DCB_df = DCB_df.ix[1:].dropna(how='any', axis=1)

# Make sure the end dates are all formatted the same and drop any NAT values
DCB_df["EndDate"] = pd.to_datetime(DCB_df['EndDate'], infer_datetime_format=True, errors='coerce') 
DCB_df = DCB_df.ix[2:]


# Find the start date for each stock by subtracting one year from the DCB date
DCB_df['StartDate'] = DCB_df.EndDate.map(lambda x: x - relativedelta(years=1))


# Convert dataframe to list of lists so we can loop through tickers and get historical data for them
DCB_list = map(list, DCB_df.values)


trading_data = open('trading_data.csv','a')

def api_call(ticker, start, end):
    prices_df = quandl.get('WIKI/'+ticker, authtoken=api_key, start_date=start, end_date=end)
    prices_df.index = pd.to_datetime(prices_df.index, infer_datetime_format=True)
    prices_df['Ticker'] = ticker
    prices_df.to_csv('trading_data.csv', mode='a', header=False)

def get_DCBprices(array):
	for row in array:
		try:
			ticker = str(row[1])
			start = str(row[2].strftime("%Y-%m-%d"))
			end = str(row[0].strftime("%Y-%m-%d"))
			print ticker + ' ' + start + ' ' + end
			api_call(ticker, start, end)
		except:
			print "Ticker does not exist in database"


#get_DCBprices(DCB_list) HAS BEEN CALLED
trading_data.close()


# Read the big list of historical data for all DCB stocks into a df.
GiantDCB_df = pd.read_csv('trading_data.csv')
GiantDCB_df.columns = ['Date', 'Open',	'High',	'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', 'Ticker']
final_DCBlist = GiantDCB_df.Ticker.unique()

DCBlist_train = []
DCBlist_test = []

def split_list(len):
	for i in range(0,len):
		if i % 2 == 0:
			DCBlist_train.append(final_DCBlist[i])
		else:
			DCBlist_test.append(final_DCBlist[i])


#split_list(len(final_DCBlist))

DCBshort_list = []

shortInterest_data = open('shortInterest_data.csv','a')

# Get number of shares that have been shorted for each stock.
def get_short_interest(array):
    for row in array:
        ticker = str(row[1])
        if ticker in final_DCBlist:
            try:
            	end = str(row[0].strftime("%Y-%m-%d"))			
            	short_df = quandl.get('SI/'+ticker+'_SI', authtoken=api_key, end_date=end)
                short_df = short_df.tail(1)
                short_df['Ticker'] = ticker
                short_df.index = pd.to_datetime(short_df.index, infer_datetime_format=True)
                short_df.to_csv('shortInterest_data.csv', mode='a', header=False)
                print ticker 
            except:
                print ticker + "Does not exist in database"
	    

#get_short_interest(DCB_list) THIS HAS BEEN CALLED
shortInterest_data.close()

# Read in the short interest data for DCB stocks into a dataframe
short_interestdf = pd.read_csv('shortInterest_data.csv', header=None)
short_interestdf.columns = ['Date','Short_Interest','Volume','Days_to_cover','Ticker']


# Function to get the % change from Yr High, Yr Low and 50 day mean
def get_DCBstats(df):
	global change_from_high, change_from_low, change_from_50dMean
	High = df.Close.max()
	current_close = df.iat[-3,4]
	change_from_high = (((current_close-High)/High)*100)
	
	Low = df.Close.min()
	change_from_low = (((current_close-Low)/Low)*100)

	fifty_daydf = df.tail(52)
	fifty_day_series = fifty_daydf.Close[0:49]
	Mean = fifty_day_series.mean()
	change_from_50dMean = (((current_close-Mean)/Mean)*100)
	


# Calculate 30d average trading volume
def get_avgvolume(df):
	global volume_mean
	vseries = df.Volume.tail(32)
	volume_series = vseries[0:29]
	volume_mean = volume_series.mean()
	



final_stats_csv = open('FinalStats.csv', 'a')

# Function to assemble all the final stats into one csv
def create_stats_csv():
	index = 1
	for ticker in final_DCBlist:
		get_DCBstats(GiantDCB_df[GiantDCB_df['Ticker']==ticker])
		get_avgvolume(GiantDCB_df[GiantDCB_df['Ticker']==ticker])
		shares_short = short_interestdf[short_interestdf['Ticker']==ticker].iat[0,1]
		temp_stats_df = pd.DataFrame({'Shares_Shorted': shares_short,
						  'Average_Volume': volume_mean,
			                          'Change_from_50day_Avg(%)': change_from_50dMean,
			                          'Change_from_Low(%)': change_from_low, 
			                          'Change_from_High(%)': change_from_high, 
			                          'Ticker': ticker,	                            
			                          },index=[index])
		print temp_stats_df.head()
		temp_stats_df.to_csv('FinalStats.csv', mode='a', header=False)
		index = index + 1
        print ticker 


#create_stats_csv() HAS BEEN CALLED
final_stats_csv.close()











