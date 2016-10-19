# The_Dead_Cat_Bounce
A study of stocks with a predictive model

## What is a Dead Cat Bounce?
A dead cat bounce is a small, short lived recovery in the price of a declining security after a significant downward trend. For example,  suppose the market (or an individual stock) has been falling over the last ten weeks but there is a broad market rally in week 11. The rally is considered a dead cat bounce if it's short-lived and the market continues to fall again in week 12. Most of the time, waffling causes a dead cat bounce. During a long downward slide, some investors may think that the market or a particular security has bottomed out. They begin buying instead of selling, or some may be closing out their short positions and pocketing gains. These factors create a little buying momentum, albeit brief. After this buying momentum is over, the stock falls again. Dead cat bounce candidates can also be identified over shorter time frames, e.g a stock that drops 5% one day and rises 3% the next

## Objective of this study
To classify stocks as candidates for a dead cat bounce based on trading metrics such as the short ratio (% of total shares that have been short sold), % change from 50 day moving average, % change from year high, etc, in the period leading up to that point. The goal is to build a model that predicts whether a certain stock is a stock that has displayed dead cat bounce behavior based on these attributes.

## Data Retrieval
I started off by manually compiling a list of about 85 or so tickers of stocks that had been reported by the Street as exhibiting a dead cat bounce over a 48-72 hour timeframe. I used this list of tickers to retrieve stock data from Quandl.com's API, which is a fantastic resource to obtain financial and economic datasets. Not all of the stocks had historical information I could pull from Quandl, leaving me with about 64 stocks I was successful in obtaining historical data for. The data represents historical prices and volume dating back to one year before the dead cat bounce was recorded. The metrics I calculated from this data are listed below:
* Change From High: Represents the % change in the closing price (taken immediately before the dead cat bounce for all metrics) to the       High for the trailing 12 months.
* Change from Low: Represents the % change in the closing price to the Low for the trailing 12 months.
* Change from Moving Average: Represents the % change in the closing price to the 50 day moving average for the trailing 50 days.
* Short Ratio: (Shares sold short / Average Daily Volume for trailing 30 days)

After creating a consolidated csv for all the Dead cat bounce stocks with the metrics I wanted, I went about obtaining the same metrics for stocks that had not shown dead cat bounce behavior (the negatives). I created a long ticker string of over 300 stocks and got the data from Yahoo Finance. I then combined the data to create a csv file named CONSOLIDATED_DCB_DATA.csv that contained the relevant information for both Dead Cat Bounce stocks (the first 64 or so rows) and Non Dead Cat Bounce stocks (the next 360 or so rows).

