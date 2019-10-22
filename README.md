# Bitcoin-Trading-Strategy
Bitcoin Simple Moving Average Trading Strategy 
Read in daily Bitcoin prices and keep the “Adj Close”.
2.Construct two rolling SMA series: T1=30 days and T2=365days
3.Keep the time period from December 31, 2012 to December 31, 2018.
4.Plot the time series of daily Bitcoin prices, SMA(T1), and SMA(T2)
5.Determine the trading position according to the signal defined above: Position=1 if SMA(T1) > SMA(T2)and Position=-1 if SMA(T1) <=SMA(T2)
6.Add the time series of Position to the plot in #4with a secondary Y-axis for Position
7.Compute the daily returns separately for (a) a passive long position in Bitcoin and(b)the SMA strategy above
8.Compute the cumulative returns over the entire period and the annualized standard deviation (based on daily returns) for the two strategies in #7
9.Find the T1 and T2 combination that delivers the highestcumulative returns. 
This step requires the use of “for” loop to backtest the SMA strategies using a range of values for T1 and T2 and then sort the strategies based on cumulative returns.
