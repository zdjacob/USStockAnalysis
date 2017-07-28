
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import quandl 
import talib
quandl.ApiConfig.api_key = "RMyHsh_ctz6QyFwTMG_z"

from scipy.stats import norm
import os

# from IPython.display import display
# from IPython.display import Markdown
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


####################################################### # Getting list of SP500 from Quandl

# In[ ]:

# SP500=pd.read_csv('https://www.quandl.com/api/v3/datatables/SHARADAR/INDEX.csv?api_key=RMyHsh_ctz6QyFwTMG_z')
# print SP500.shape
# SP500=SP500[SP500['removed'].isnull()]
# SP500=SP500.sort_values(['ticker'])
# SP500.reset_index(inplace=True,drop=True)
# SP500.head()


####################################################### # Not WORKING: Yahoo Finance data

# In[ ]:

# from yahoo_finance import Share

# fundamentalData=pd.DataFrame(SP500['ticker'])
# for index, row in fundamentalData.iterrows():
    
#     sharePrice = Share(row['ticker'])
#     fundamentalData.set_value(index, 'SharePrice',sharePrice.get_price())
#     fundamentalData.set_value(index, 'Year52High',sharePrice.get_year_high())
#     fundamentalData.set_value(index, 'Year52Low',sharePrice.get_year_low())
#     fundamentalData.set_value(index, 'ChangeFromHigh',sharePrice.get_percent_change_from_year_high())
#     fundamentalData.set_value(index, 'ChangeFromLow',sharePrice.get_percent_change_from_year_low())
#     fundamentalData.set_value(index, 'PE',sharePrice.get_price_earnings_ratio())
#     fundamentalData.set_value(index, 'EPS',sharePrice.get_earnings_share())


    
#     fundamentalData.set_value(index, 'PEG',sharePrice.get_price_earnings_growth_ratio())
    
    
    
# fundamentalData


# # Quandl free data analysis

####################################################### Single Stock Testing

# In[ ]:

stockCode='A'
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
revenueGrowth=talib.ROC(np.asarray(REVENUEUSD.Value), timeperiod=1)
revenueGrowth = revenueGrowth[-3:][~np.isnan(revenueGrowth[-3:])]    
meanRevenueGrowthRate=revenueGrowth.mean()
print 'Mean Revenue growth :: ',meanRevenueGrowthRate

print '\n**************** GP ****************************'
GP=quandl.get('SF0/'+stockCode+'_GP_MRY')
currentGP=GP.Value[-1]
GPMargin=GP/REVENUEUSD
currentGPMargin=GPMargin.Value[-1]
print 'GP',GP
print 'GPMargin',GPMargin
print 'GPMarginMean',GPMargin.mean()
print 'currentGPMargin',currentGPMargin

print '\n**************** NETINC ****************************'
NETINC=quandl.get('SF0/'+stockCode+'_NETINC_MRY')
currentNETINC=NETINC.Value[-1]
NETINCMargin=NETINC/REVENUEUSD
currentNETINCMargin=NETINCMargin.Value[-1]
print 'NETINC',NETINC
print 'NETINCMargin',NETINCMargin
print 'NETINCMargin',NETINCMargin.mean()
print 'currentNETINCMargin',currentNETINCMargin


print '\n**************** ROE ****************************'
EQUITY=quandl.get('SF0/'+stockCode+'_EQUITY_MRY')
currentEQUITY=EQUITY.Value[-1]
ROE=NETINC/EQUITY
currentROE=ROE.Value[-1]
print 'EQUITY',EQUITY
print 'ROE',ROE
print 'ROE_MEAN',ROE.mean()
print 'currentROE',currentROE

print '\n**************** ROA ****************************'
ASSETS=quandl.get('SF0/'+stockCode+'_ASSETS_MRY')
currentASSETS=ASSETS.Value[-1]
ROA=NETINC/ASSETS
currentROA=ROA.Value[-1]
print 'ASSETS',ASSETS
print 'ROA',ROA
print 'ROA_MEAN',ROA.mean()
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


# In[ ]:




# In[ ]:




####################################################### # SF1 Paid Data from Quandl - NOT WORKING YET

# # In[ ]:

# fundamentalData=SP500[['ticker']]
# for index, row in fundamentalData.iterrows():
#     print row['ticker']
#     downloadLink='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+row['ticker']+'&qopts.columns=date,open&api_key=RMyHsh_ctz6QyFwTMG_z'
#     SF1Data=pd.read_csv(downloadLink)
#     pd.set_option('display.max_columns', None)
#     print SF1Data
# #     SF1Data=SF1Data.iloc[-1,:]
# #     fundamentalData[index,'roe']=SF1Data['roe']
# #     fundamentalData[index,'roa']=SF1Data['roa']
# #     fundamentalData[index,'roic']=SF1Data['roic']
# #     fundamentalData[index,'ros']=SF1Data['ros']
# #     fundamentalData[index,'sps']=SF1Data['sps']
# #     fundamentalData[index,'pb']=SF1Data['pb']
# #     fundamentalData[index,'pe']=SF1Data['pe']
# #     fundamentalData[index,'netmargine']=SF1Data['netmargin']
# #     fundamentalData[index,'grossmargin']=SF1Data['grossmargin']
# #     fundamentalData[index,'de']=SF1Data['de']
# #     fundamentalData[index,'cashnequsd']=SF1Data['cashnequsd']
# #     fundamentalData[index,'epsusd']=SF1Data['epsusd']
# fundamentalData

