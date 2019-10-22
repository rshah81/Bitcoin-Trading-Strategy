#!/usr/bin/env python
# coding: utf-8

# Rishabh Shah 

# In[1]:


#Trading based on simple moving averages (SMAs) is one of the oldest algorithmic trading strategies.
#Traders construct two moving averages with different length: T1 and T2, where T1 < T2. The trading signal is given by:
#Signal = Establish long/liquidate short position if SMA(T1) > SMA(T2)
#Establish short/liquidate long position if SMA(T1) < SMA(T2)


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import seaborn as sns
import statsmodels.formula.api as smf
from scipy.stats import norm
from itertools import product 


# In[3]:


#1 Read in daily Bitcoin prices and keep the “Adj Close”
bit_prices = pd.DataFrame()
bit_prices = pd.read_csv('BTC_DailyPrice_USD.csv',parse_dates = True, index_col = "Date")
bit_prices = bit_prices['Adj Close']
print(bit_prices.tail())


# In[4]:


# Take log of daily bitcoin returns
bit_returns = np.log(bit_prices/bit_prices.shift(1))
bit_returns.rename(columns = {'Adj Close': 'ret_bit'}, inplace = True)
bit_returns.dropna(inplace = True)
print(bit_returns.tail())


# In[5]:


#2. Construct two rolling SMA series: T1=30 days and T2=365 days
t1= bit_prices.rolling(window=30).mean()
t1.rename(columns = {'Adj Close': '30'}, inplace = True)
print(t1.tail())
t2= bit_prices.rolling(window =365).mean()
t2.rename(columns = {'Adj Close': '365'}, inplace = True)
print(t2.tail())


# In[6]:


#3 Keep the time period from December 31, 2012 to December 31, 2018. Is this inclusive or not?
t1 = t1[(t1.index >= '2012-12-31') & (t1.index <= '2018-12-31')]
print(t1.head())
t2 = t2[(t2.index >= '2012-12-31') & (t2.index <= '2018-12-31')]
print(t2.head())
bit_returns = bit_returns[(bit_returns.index >= '2012-12-31') & (bit_returns.index <= '2018-12-31')]
print(bit_returns.head())


# In[7]:


#4 Plot the time series of daily Bitcoin prices, SMA(T1), and SMA(T2)
print(bit_prices.plot())
print(t1.plot())
print(t2.plot())


# In[8]:


#5 Determine the trading position according to the signal defined above: Position=1 if 
#SMA(T1) > SMA(T2) and Position=-1 if SMA(T1) <= SMA(T2)
t3 = pd.concat([bit_returns,t1,t2], axis =1)
t3.rename(columns = {'0': 'Bit_returns', '1': 'SMA T1', '2': 'SMA T2'}, inplace = True)
t3['Position'] = np.where(t3[1] > t3[2], 1,-1)
print(t3.head())


# In[9]:


#6 Add the time series of Position to the plot in #4 with a secondary Y-axis for Position
print(bit_prices.plot())
print(t1.plot())
print(t2.plot())
print(t3['Position'].plot(secondary_y = True))

#ax = {(bit_prices, t1, t2)}.plot()
#ax2 = df['Position'].plot(secondary_y=True)
#ax2.set_ylim(-20, 50)
#fig = ax.get_figure()
#fig.savefig('test.png')


# In[10]:


#7  Part A Compute the daily returns separately for (a) a passive long position in Bitcoin 
# Take log of daily bitcoin returns
# repeat of code from above 
bit_returns = np.log(bit_prices/bit_prices.shift(1))
bit_returns.rename(columns = {'Adj Close': 'ret_bit'}, inplace = True)
bit_returns.dropna(inplace = True)
print(bit_returns.head())


# In[11]:


#7 Part B the daily returns separately for the SMA strategy above
t3['SMA_Strategy'] = t3[0] * t3['Position'].shift(1)
t3.tail()


# In[12]:


#8 Compute the cumulative returns over the entire period and the annualized standard deviation (based on daily returns) for the two strategies in #7
print('SMA Cumulative Returns')
print(t3[['SMA_Strategy']].sum().apply(np.exp))
print('Passive Bitcoin Cumulative Return')
print(t3[[0]].sum().apply(np.exp))

print('Annualized Std. Deviation Passive Bitcoin')
print(t3[[0]].std()*(252**0.5))
print('SMA Annualized Std. Deviations')
print(t3[['SMA_Strategy']].std()*(252**0.5))


# In[24]:


#9. Find the T1 and T2 combination that delivers the highest cumulative returns. This step requires the use of “for” loop to back test the SMA strategies using a range of values for T1 and T2 and then sort the strategies based on cumulative returns.

#specify range for short and long window 
sma1 = range(7,92,7)
sma2 = range(180,363,14)
opt_backtest = pd.DataFrame()
# use product function to make pairs
for SMA_T1, SMA_T2, in product(sma1, sma2):
#create new dataframe because I couldnt use the old one becuase kept getting axis error 
    t4 = pd.DataFrame()
    t4['Bit_Returns'] = np.log(bit_prices/bit_prices.shift(1))
    t4['SMA1'] = bit_prices.rolling(window=SMA_T1).mean()
    t4['SMA2'] = bit_prices.rolling(window=SMA_T2).mean()
    t4['Position'] = np.where(t4['SMA1'] > t4['SMA2'], 1,-1)
    t4['SMA_Strategy'] = t4['Position'].shift(1) * t4['Bit_Returns'] 
    t4 = t4[(t4.index >= '2012-12-31') & (t4.index <= '2018-12-31')]
    cum_ret = t4[['Bit_Returns','SMA_Strategy']].sum().apply(np.exp) 
    opt_backtest = opt_backtest.append(pd.DataFrame({'SMA1': SMA_T1,'SMA2':SMA_T2,'Values Diff':cum_ret['SMA_Strategy'] - cum_ret ['Bit_Returns']},index=[0]) ,ignore_index=True)
      
opt_backtest.sort_values('Values Diff', ascending = False).head()


# In[25]:


opt_backtest.max()


# In[ ]:




