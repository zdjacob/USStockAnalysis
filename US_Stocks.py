
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import quandl 
import talib
quandl.ApiConfig.api_key = "RMyHsh_ctz6QyFwTMG_z"

from scipy.stats import norm
import os

from IPython.display import display
from IPython.display import Markdown
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import pprint
import warnings
warnings.filterwarnings("ignore")

from yahoo_finance import Share
from googlefinance import getQuotes
import json

import plotly
plotly.offline.init_notebook_mode() # run at the start of every ipython notebook
import plotly.offline as py
import plotly.graph_objs as go


# # Getting list of SP500 from Quandl

# In[ ]:

SP500=pd.read_csv('https://www.quandl.com/api/v3/datatables/SHARADAR/INDEX.csv?api_key=RMyHsh_ctz6QyFwTMG_z')
print SP500.shape
SP500=SP500[SP500['removed'].isnull()]
SP500=SP500.sort_values(['ticker'])
SP500.reset_index(inplace=True,drop=True)
SP500.head()


# # Not WORKING: Yahoo Finance data

# In[ ]:

from yahoo_finance import Share

fundamentalData=pd.DataFrame(SP500['ticker'])
for index, row in fundamentalData.iterrows():
    
    sharePrice = Share(row['ticker'])
    fundamentalData.set_value(index, 'SharePrice',sharePrice.get_price())
    fundamentalData.set_value(index, 'Year52High',sharePrice.get_year_high())
    fundamentalData.set_value(index, 'Year52Low',sharePrice.get_year_low())
    fundamentalData.set_value(index, 'ChangeFromHigh',sharePrice.get_percent_change_from_year_high())
    fundamentalData.set_value(index, 'ChangeFromLow',sharePrice.get_percent_change_from_year_low())
    fundamentalData.set_value(index, 'PE',sharePrice.get_price_earnings_ratio())
    fundamentalData.set_value(index, 'EPS',sharePrice.get_earnings_share())


    
    fundamentalData.set_value(index, 'PEG',sharePrice.get_price_earnings_growth_ratio())
    
    
    
fundamentalData


# # Quandl free data analysis

# # Single Stock Testing

# In[ ]:

stockCode='ZAYO'
data = quandl.get_table('WIKI/PRICES', ticker = stockCode)

try:
    data = quandl.get_table('WIKI/PRICES', ticker = stockCode, date = { 'gte': '1980-01-01' })

    if data.empty:
        #currentSharePrice=float(getQuotes(stockCode)[0]['LastTradePrice'])
        sharePrice = Share(stockCode)
        currentSharePrice=float(sharePrice.get_price())
        week52High= float(sharePrice.get_year_high())
        week52Low= float(sharePrice.get_year_low())
        volume10DAvg=float(sharePrice.get_avg_daily_volume())
    else:
        range52WeekPrice=data.adj_close[-252:]
        currentSharePrice=data[-1:]['adj_close'].values[0]
        week52High=range52WeekPrice.max()
        week52Low=range52WeekPrice.min()

        range10DayVol=data[-10:]['volume']
        volume10DAvg=range10DayVol.mean()
except:
    print stockCode

ChangeFromHigh=(week52High-currentSharePrice)/currentSharePrice
ChangeFromLow=(currentSharePrice-week52Low)/currentSharePrice

print 'currentSharePrice',currentSharePrice
print 'week52High',week52High
print 'week52Low',week52Low
print 'ChangeFromHigh',ChangeFromHigh
print 'ChangeFromLow',ChangeFromLow
print 'volume10DAvg',volume10DAvg


print '\n**************** EPS ****************************'
EPS=quandl.get('SF0/'+stockCode+'_EPSUSD_MRY')
currentEPS=EPS.Value[-1]
EPSGrowthRate=(EPS.Value[-1]-EPS.Value[-2])/EPS.Value[-2]
PE=currentEPS/currentSharePrice
print 'EPS',EPS
print 'currentEPS',currentEPS
print 'EPSGrowthRate',EPSGrowthRate
print 'PE',PE

print '\n**************** REVENUEUSD ****************************'
REVENUEUSD=quandl.get('SF0/'+stockCode+'_REVENUEUSD_MRY')
currentREVENUEUSD=REVENUEUSD.Value[-1]
REVENUEUSDGrowthRate=(REVENUEUSD.Value[-1]-REVENUEUSD.Value[-2])/REVENUEUSD.Value[-2]
print 'REVENUEUSD',REVENUEUSD
print 'currentREVENUEUSD',currentREVENUEUSD
print 'REVENUEUSDGrowthRate',REVENUEUSDGrowthRate

print '\n**************** GP ****************************'
GP=quandl.get('SF0/'+stockCode+'_GP_MRY')
currentGP=GP.Value[-1]
GPMargin=GP/REVENUEUSD
currentGPMargin=GPMargin.Value[-1]
print 'GP',GP
print 'GPMargin',GPMargin
print 'currentGPMargin',currentGPMargin

print '\n**************** NETINC ****************************'
NETINC=quandl.get('SF0/'+stockCode+'_NETINC_MRY')
currentNETINC=NETINC.Value[-1]
NETINCMargin=NETINC/REVENUEUSD
currentNETINCMargin=NETINCMargin.Value[-1]
print 'NETINC',NETINC
print 'NETINCMargin',NETINCMargin
print 'currentNETINCMargin',currentNETINCMargin


print '\n**************** EQUITY ****************************'
EQUITY=quandl.get('SF0/'+stockCode+'_EQUITY_MRY')
currentEQUITY=EQUITY.Value[-1]
ROE=NETINC/EQUITY
currentROE=ROE.Value[-1]
print 'EQUITY',EQUITY
print 'ROE',ROE
print 'currentROE',currentROE

print '\n**************** ASSETS ****************************'
ASSETS=quandl.get('SF0/'+stockCode+'_ASSETS_MRY')
currentASSETS=ASSETS.Value[-1]
ROA=NETINC/ASSETS
currentROA=ROA.Value[-1]
print 'ASSETS',ASSETS
print 'ROA',ROA
print 'currentROA',currentROA

print '\n**************** DEBT ****************************'
DEBT=quandl.get('SF0/'+stockCode+'_DEBT_MRY')
currentDEBT=DEBT.Value[-1]
DE=DEBT/EQUITY
currentDE=DE.Value[-1]
print 'DEBT',DEBT
print 'DE',DE
print 'currentDE',currentDE


print '\n**************** RND ****************************'
RND=quandl.get('SF0/'+stockCode+'_RND_MRY')
currentRND=RND.Value[-1]
RNDTOREV=RND/REVENUEUSD
currentRNDTOREV=RNDTOREV.Value[-1]
print 'RND',RND
print 'RNDTOREV',RNDTOREV
print 'currentRNDTOREV',currentRNDTOREV

print '\n**************** SHARESWA ****************************'
SHARESWA=quandl.get('SF0/'+stockCode+'_SHARESWA_MRY')
currentSHARESWA=SHARESWA.Value[-1]
print 'SHARESWA',SHARESWA
print 'currentSHARESWA',currentSHARESWA

print '\n**************** CASHNEQ ****************************'
CASHNEQUSD=quandl.get('SF0/'+stockCode+'_CASHNEQUSD_MRY')
currentCASHNEQUSD=CASHNEQUSD.Value[-1]
print 'CASHNEQUSD',CASHNEQUSD
print 'currentCASHNEQUSD',currentCASHNEQUSD

print '\n**************** DPS ****************************'
DPS=quandl.get('SF0/'+stockCode+'_DPS_MRY')
currentDPS=DPS.Value[-1]
dividendYeild=currentDPS/currentSharePrice
print 'DPS',DPS
print 'currentDPS',currentDPS
print 'dividendYeild',dividendYeild


# # Quandl combined with yahoo finance complete analysis for Quandl 2000 companies
# 
# 

# In[1]:

import pandas as pd
import numpy as np
import quandl 
quandl.ApiConfig.api_key = "RMyHsh_ctz6QyFwTMG_z"

from scipy.stats import norm
import os

from IPython.display import display
from IPython.display import Markdown
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import pprint
import warnings
warnings.filterwarnings("ignore")

from yahoo_finance import Share
from googlefinance import getQuotes
import json


# In[12]:

fundamentalData=pd.read_csv('http://www.sharadar.com/meta/sf0-tickers.txt',sep ='\t')
#fundamentalData=pd.read_csv('sf0-tickers.txt',sep ='\t')
fundamentalData=fundamentalData[['Ticker','Name','Currency','Sector','Industry','Exchange']]

pd.set_option('display.max_columns', None)
timeZero=pd.datetime.now()
yahooCounter=0
wikiCounter=0
for index, row in fundamentalData.iterrows():
    startTime=pd.datetime.now()
    stockCode= row['Ticker']
    exchange=row['Exchange']

    if exchange=='DELISTED':
        continue
    try:
        data = quandl.get_table('WIKI/PRICES', ticker = stockCode, date = { 'gte': '2005-01-01' })

        if data.empty:
            #currentSharePrice=float(getQuotes(stockCode)[0]['LastTradePrice'])
            sharePrice = Share(stockCode)
            currentSharePrice=float(sharePrice.get_price())
            week52High= float(sharePrice.get_year_high())
            week52Low= float(sharePrice.get_year_low())
            volume10DAvg=float(sharePrice.get_avg_daily_volume())
            yahooCounter=yahooCounter+1
        else:
            range52WeekPrice=data.adj_close[-252:]
            currentSharePrice=data[-1:]['adj_close'].values[0]
            week52High=range52WeekPrice.max()
            week52Low=range52WeekPrice.min()

            range10DayVol=data[-10:]['volume']
            volume10DAvg=range10DayVol.mean()
            wikiCounter=wikiCounter+1


        ChangeFromHigh=(week52High-currentSharePrice)/currentSharePrice
        ChangeFromLow=(currentSharePrice-week52Low)/currentSharePrice

        EPS=quandl.get('SF0/'+stockCode+'_EPSUSD_MRY')
        currentEPS=EPS.Value[-1]
        EPSGrowthRate=(EPS.Value[-1]-EPS.Value[-2])/EPS.Value[-2]
        currentPE=currentSharePrice/currentEPS
        currentPEtoGrowth=currentPE/(EPSGrowthRate*100.)
        
        
        REVENUEUSD=quandl.get('SF0/'+stockCode+'_REVENUEUSD_MRY')
        currentREVENUEUSD=REVENUEUSD.Value[-1]/1000000.
        REVENUEUSDGrowthRate=(REVENUEUSD.Value[-1]-REVENUEUSD.Value[-2])/REVENUEUSD.Value[-2]

        GP=quandl.get('SF0/'+stockCode+'_GP_MRY')
        currentGP=GP.Value[-1]
        GPMargin=GP/REVENUEUSD
        currentGPMargin=GPMargin.Value[-1]

        NETINC=quandl.get('SF0/'+stockCode+'_NETINC_MRY')
        currentNETINC=NETINC.Value[-1]
        NETINCMargin=NETINC/REVENUEUSD
        currentNETINCMargin=NETINCMargin.Value[-1]

        EQUITY=quandl.get('SF0/'+stockCode+'_EQUITY_MRY')
        currentEQUITY=EQUITY.Value[-1]
        ROE=NETINC/EQUITY
        currentROE=ROE.Value[-1]

        ASSETS=quandl.get('SF0/'+stockCode+'_ASSETS_MRY')
        currentASSETS=ASSETS.Value[-1]
        ROA=NETINC/ASSETS
        currentROA=ROA.Value[-1]

        DEBT=quandl.get('SF0/'+stockCode+'_DEBT_MRY')
        currentDEBT=DEBT.Value[-1]
        DE=DEBT/EQUITY
        currentDE=DE.Value[-1]

        RND=quandl.get('SF0/'+stockCode+'_RND_MRY')
        currentRND=RND.Value[-1]
        RNDTOREV=RND/REVENUEUSD
        currentRNDTOREV=RNDTOREV.Value[-1]

        SHARESWA=quandl.get('SF0/'+stockCode+'_SHARESWA_MRY')
        currentSHARESWA=SHARESWA.Value[-1]//1000000.

        DPS=quandl.get('SF0/'+stockCode+'_DPS_MRY')
        currentDPS=DPS.Value[-1]
        dividendYeild=currentDPS/currentSharePrice
        
        marketCap=currentSHARESWA*currentSharePrice
        priceToSales=marketCap/currentREVENUEUSD
        
        fundamentalData.set_value(index,'currentSharePrice',currentSharePrice)
        fundamentalData.set_value(index,'week52High',week52High)
        fundamentalData.set_value(index,'week52Low',week52Low)
        fundamentalData.set_value(index,'changeFromHigh',ChangeFromHigh)
        fundamentalData.set_value(index,'changeFromLow',ChangeFromLow)
        fundamentalData.set_value(index,'marketCapMil',marketCap)
        fundamentalData.set_value(index,'volume10DAvg',volume10DAvg)

        fundamentalData.set_value(index,'eps',currentEPS)
        fundamentalData.set_value(index,'epsGrowthRate',EPSGrowthRate)
        fundamentalData.set_value(index,'pe',currentPE)
        fundamentalData.set_value(index,'priceToSales',priceToSales)
        fundamentalData.set_value(index,'petoGrowth',currentPEtoGrowth)
        fundamentalData.set_value(index,'dividendYeild',dividendYeild)
        
        fundamentalData.set_value(index,'revenueMil',currentREVENUEUSD)
        fundamentalData.set_value(index,'revenueGrowthRate',REVENUEUSDGrowthRate)

        fundamentalData.set_value(index,'nettMargin',currentNETINCMargin)
        fundamentalData.set_value(index,'gpMargin',currentGPMargin)

        fundamentalData.set_value(index,'roe',currentROE)
        fundamentalData.set_value(index,'roa',currentROA)
        fundamentalData.set_value(index,'de',currentDE)
        fundamentalData.set_value(index,'rndtorev',currentRNDTOREV)
        fundamentalData.set_value(index,'numOfSharesMil',currentSHARESWA)
    except:
        print stockCode
    if(index%100==0):
        endTime=pd.datetime.now()
        print '****Completed ', index, ' number of shares.',float(index)/len(fundamentalData),'% completed'
        print '****Time for analysing 100 shares :: ' ,endTime-startTime,', Time from zero ::',endTime-timeZero,', Time Now :: ',endTime.time()
print 'Completed :: ' ,wikiCounter,yahooCounter
fundamentalData.to_csv('USStocksData.csv',index =False)


# In[14]:

usStocks=pd.read_csv('USStocksData.csv')
usStocks.dropna(inplace=True)
usStocks=usStocks[usStocks.epsGrowthRate.str.contains("#NAME?") == False]
usStocks=usStocks[usStocks.petoGrowth.str.contains("#NAME?") == False]

usStocks.epsGrowthRate=usStocks.epsGrowthRate.astype(dtype='float64')
usStocks.nettMargin=usStocks.nettMargin.astype(dtype='float64')
usStocks.petoGrowth=usStocks.petoGrowth.astype(dtype='float64')


goodStocks=usStocks[(usStocks['changeFromHigh']<0.1) & 
         (usStocks['epsGrowthRate']>0.08)  & 
        (usStocks['revenueGrowthRate']>0.05)  &
        (usStocks['nettMargin']>0.05) & 
        (usStocks['gpMargin']>0.1) & 
        (usStocks['roe']>0.1) & 
        (usStocks['roa']>0.03) & 
        (usStocks['de']<2.)  ]




goodStocks.to_csv('US_GoodStocks.csv',index =False)

#print goodStocks.dtypes
goodStocks.sort_values(ascending=0,by='marketCapMil',inplace=True)
goodStocks.reset_index(inplace=True,drop =True)
largeCapGoodOnes=goodStocks[:25]
# display(largeCapGoodOnes)

goodStocks.sort_values(ascending=0,by='dividendYeild',inplace=True)
goodStocks.reset_index(inplace=True,drop =True)
dividendYeildGoodOnes=goodStocks[:25]
# display(dividendYeildGoodOnes)

goodStocks.sort_values(ascending=0,by='roe',inplace=True)
goodStocks.reset_index(inplace=True,drop =True)
roeGoodOnes=goodStocks[:25]
# display(roeGoodOnes)

goodStocks.sort_values(ascending=0,by='nettMargin',inplace=True)
goodStocks.reset_index(inplace=True,drop =True)
nettMarginGoodOnes=goodStocks[:25]
# display(nettMarginGoodOnes)

finalList=pd.concat([largeCapGoodOnes,dividendYeildGoodOnes,roeGoodOnes,nettMarginGoodOnes]).drop_duplicates().reset_index(drop=True)
finalList.sort_values(ascending=0,by='marketCapMil',inplace=True)
finalList.reset_index(inplace=True,drop =True)
finalList.to_csv('US_StocksToInvest.csv',index =False)
display(finalList.describe())
display(finalList)


# In[11]:

def countConseq(negativeStockReturns):
    count=0
    for i in range(len(negativeStockReturns)-1,0,-1):
        if(negativeStockReturns[i]==True):
            count=count+1
        else:
            break
    return count

def checkTurnAround(negativeStockReturns):
    if(negativeStockReturns[-1]==False):
        negativesBeforeTurnaround=countConseq(negativeStockReturns[:-1])
        return True,negativesBeforeTurnaround
    else:
        return False,0
    


# # Building Technical Analysis on top of Good Stocks

# In[15]:

printer=False
for index,row in goodStocks.iterrows():
    
    stockCode=row['Ticker']
    #print "Processing :: ",stockCode," Count :: ",index+1
    try:
        stockPrice=quandl.get_table('WIKI/PRICES', ticker = stockCode, date = { 'gte': '2010-01-01' })
        
        priceThen = quandl.get_table('WIKI/PRICES', ticker = stockCode, date = '2016-11-01').iloc[-1]['adj_close']
        priceNow = quandl.get_table('WIKI/PRICES', ticker = stockCode, date = '2017-07-25').iloc[-1]['adj_close']
        returns=(priceNow-priceThen)/float(priceThen)
        
        
        stockPrice.dropna(inplace=True)
        close=np.asarray(stockPrice.close)
        open=np.asarray(stockPrice.open)
        low=np.asarray(stockPrice.low)
        high=np.asarray(stockPrice.high)
        volume=np.asarray(stockPrice.volume)

        SMA10 = talib.SMA(close,timeperiod=10)  
        SMA50 = talib.SMA(close,timeperiod=50)

        SMA10Vol=talib.SMA(volume,timeperiod=10)
        SMA5Vol=talib.SMA(volume,timeperiod=5)

        MOM14 = talib.MOM(close, timeperiod=14)

        RSI14 = talib.RSI(close, timeperiod=14)
    except:
        print '*********************Error in processing*********************', stockCode
        continue


    # slowk, slowd =  talib.STOCH(high, low, close, fastk_period=14, slowk_period=14,  slowd_period=14, slowk_matype=0, slowd_matype=0)

    # print "Slow K indicator Share Price :: ",'\n',  slowk[-10:]
    # print "Slow D indicator Share Price :: ",'\n',  slowd[-10:]

    fastk, fastd= talib.STOCHF(high, low, close,fastd_matype=0,fastd_period=5,fastk_period=14) 

    dailyReturns = talib.ROC(close, timeperiod=1)

    negativeStockReturns=dailyReturns<0


    conseqNegativeDays=countConseq(negativeStockReturns)
    #display(negativeStockReturns)
    turnaroundChecker=checkTurnAround(negativeStockReturns)
    turnaround=turnaroundChecker[0]
    afterHowManyDays=turnaroundChecker[1]
    
    yearlyReturn=(stockPrice.iloc[-1].close/stockPrice.iloc[-252].close)-1
    quarterlyReturn=(stockPrice.iloc[-1].close/stockPrice.iloc[-63].close)-1           
    monthlyReturn=(stockPrice.iloc[-1].close/stockPrice.iloc[-21].close)-1
                   
    if(conseqNegativeDays>0):
        drawDown=talib.ROC(close, timeperiod=conseqNegativeDays)
        goodStocks.set_value(index, 'drawDown', drawDown[-1])
    if printer:
        print "Tail of Share Price :: ",'\n'
        display(stockPrice.tail())
        print "SMA 30 of Share Price :: ",'\n'
        display(SMA10[-10:])
        print "SMA 50 of Share Price :: ", '\n'
        display(SMA50[-10:])
        print "SMA 10 day Volume average :: ",'\n'
        display(SMA10Vol[-10:])
        print "SMA 5 of Volume average :: ", '\n'
        display(SMA5Vol[-10:])
        print "Momentum indicator Share Price :: ",'\n'
        display(MOM14[-10:])
        print "RSI indicator Share Price :: ",'\n'
        display(RSI14[-10:])
        print "Fast K indicator Share Price :: ",'\n'
        display(fastk[-10:])
        print "Fast D indicator Share Price :: ",'\n'
        display(fastd[-10:]),'\n' # D is the Signal line
        print "Daily Returns for Share Price :: ",'\n'
        display(dailyReturns[-10:])
        print stockCode,conseqNegativeDays
        print "Number of consequtive negative days :: ",'\n',conseqNegativeDays,'\n'
        if(conseqNegativeDays>0):
            print "Returns during the downward phase   :: ",'\n',drawDown[-1:],'\n'
        print "Is there a Turnaround :: ",turnaround,'\n'
        print "Number of days after which stock turned around  ",afterHowManyDays,'\n'
    
    goodStocks.set_value(index, 'dailyReturns', dailyReturns[-1])
    goodStocks.set_value(index, 'Close', close[-1])
    goodStocks.set_value(index, 'Day5AvgVol', SMA5Vol[-1])
    goodStocks.set_value(index, 'Day10AvgVol', SMA10Vol[-1])
    goodStocks.set_value(index, 'Volume', volume[-1])
    goodStocks.set_value(index, 'returnsFromNov', returns)

    goodStocks.set_value(index, 'YearlyReturn', yearlyReturn)
    goodStocks.set_value(index, 'QuarterlyReturn', quarterlyReturn)
    goodStocks.set_value(index, 'MonthlyReturn', monthlyReturn)
    
    goodStocks.set_value(index, 'RSI14', RSI14[-1])
    goodStocks.set_value(index, 'SMA10', SMA10[-1])
    goodStocks.set_value(index, 'SMA50', SMA50[-1])
    
    goodStocks.set_value(index, 'MOM14', MOM14[-1])
    goodStocks.set_value(index, 'fastk', fastk[-1])
    goodStocks.set_value(index, 'fastd', fastd[-1])
    
    goodStocks.set_value(index, 'turnaround', turnaround)
    goodStocks.set_value(index, 'afterHowManyDays', afterHowManyDays)
    
    goodStocks.set_value(index, 'conseqNegativeDays', conseqNegativeDays)

goodStocks.to_csv('US_GoodStocksWithTechnical.csv')
display(goodStocks.describe())
print 'Completed Technical Analysis'  


# In[ ]:

goodStocks.loc[goodStocks.returnsFromNov<0.05]


# In[6]:

print 'BUY :: Turning around after more than 3 days of negative momentum \n'
display(goodStocks.loc[(goodStocks.turnaround==True) & (goodStocks.afterHowManyDays>3)])

print 'WATCH :: Stocks with more than 3 days of negative move \n'
display(goodStocks.loc[goodStocks.conseqNegativeDays>3])

print 'BUY:: Stocks with RSI less than 40'
display(goodStocks.loc[goodStocks.RSI14<40])

print 'SELL :: Stocks with RSI more than 70'
display(goodStocks.loc[goodStocks.RSI14>70])

print 'SELL :: Stocks with MOM more than 90'
display(goodStocks.loc[goodStocks.fastk>90])

print 'BUY :: Stocks with MOM less than 10'
display(goodStocks.loc[goodStocks.fastk<10])

print 'BUY :: Stocks with yearly returns > 30%'
display(goodStocks.loc[goodStocks.YearlyReturn>.3])

print 'BUY :: Stocks with quarterly returns > 30%'
display(goodStocks.loc[goodStocks.QuarterlyReturn>.3])

print 'BUY :: Stocks with monthly returns > 30%'
display(goodStocks.loc[goodStocks.MonthlyReturn>.3])


print 'WATCH :: Stocks with more than 2 times the 10 day Volume'
display(goodStocks.loc[goodStocks.Volume>2*goodStocks.Day10AvgVol])

print 'WATCH :: Stocks with more than 2 times the 5 day Volume'
display(goodStocks.loc[goodStocks.Volume>2*goodStocks.Day5AvgVol])


# In[ ]:




# In[ ]:




# # SF1 Paid Data from Quandl - NOT WORKING YET

# In[ ]:

fundamentalData=SP500[['ticker']]
for index, row in fundamentalData.iterrows():
    print row['ticker']
    downloadLink='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+row['ticker']+'&qopts.columns=date,open&api_key=RMyHsh_ctz6QyFwTMG_z'
    SF1Data=pd.read_csv(downloadLink)
    pd.set_option('display.max_columns', None)
    print SF1Data
#     SF1Data=SF1Data.iloc[-1,:]
#     fundamentalData[index,'roe']=SF1Data['roe']
#     fundamentalData[index,'roa']=SF1Data['roa']
#     fundamentalData[index,'roic']=SF1Data['roic']
#     fundamentalData[index,'ros']=SF1Data['ros']
#     fundamentalData[index,'sps']=SF1Data['sps']
#     fundamentalData[index,'pb']=SF1Data['pb']
#     fundamentalData[index,'pe']=SF1Data['pe']
#     fundamentalData[index,'netmargine']=SF1Data['netmargin']
#     fundamentalData[index,'grossmargin']=SF1Data['grossmargin']
#     fundamentalData[index,'de']=SF1Data['de']
#     fundamentalData[index,'cashnequsd']=SF1Data['cashnequsd']
#     fundamentalData[index,'epsusd']=SF1Data['epsusd']
fundamentalData

