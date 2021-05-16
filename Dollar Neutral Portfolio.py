import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from winreg import *





with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
    Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

if os.path.exists(Downloads+"\constituents_csv.csv"):
  os.remove(Downloads+"\constituents_csv.csv")
else:
  print("The file does not exist")

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://datahub.io/core/s-and-p-500-companies#resource-constituents")

element = driver.find_element_by_link_text("csv (19kB)")
element.click();

Download=  Downloads + '\constituents_csv.csv'





SPdata=pd.pandas.read_csv(Download)





import yfinance as yf
print('Completed :')
for x in range(504):
    ticker = SPdata["Symbol"].iloc[x]
    
    if "." in ticker:
        print(ticker + " not counted")
    else:
        def yfinancetut(tickersymbol):
            tickerdata = yf.Ticker(tickersymbol)
            tickerinfo = tickerdata.info
            hist = tickerdata.history(period="1Y")


            beta_info = tickerinfo['beta']
            
            if 'priceToBook' in tickerinfo:
                pricetobook_info= tickerinfo['priceToBook']
                SPdata.loc[SPdata.index[x], 'Price to Book'] = pricetobook_info
            else:
                SPdata.loc[SPdata.index[x], 'Price to Book'] = np.nan

                
            mean_info = hist['Close'].mean()
            standdev_info = hist['Close'].std(axis = 0, skipna = True)
            lastclose_info = hist['Close'].iloc[-1]
            zscore_info = ((lastclose_info - mean_info)/standdev_info)


            SPdata.loc[SPdata.index[x], 'Beta'] = beta_info
            
            SPdata.loc[SPdata.index[x], 'Z-Score'] = zscore_info
            print (x)
        yfinancetut(ticker)




SPdata.to_csv ('updated_values.csv', index = False, header=True)





UPdata=pd.pandas.read_csv('updated_values.csv')





for x in range(504):
    if -1 < UPdata["Beta"].iloc[x] < 2.8:
        UPdata.loc[UPdata.index[x], 'refined_beta'] = UPdata["Beta"].iloc[x]
    else:
        UPdata.loc[UPdata.index[x], 'refined_beta'] = np.nan





for x in range(504):
    UPdata.loc[UPdata.index[x], 'log_pb'] = math.log(UPdata["Price to Book"].iloc[x], 10)
    
    if -1 < UPdata["log_pb"].iloc[x] < 1.5:
        UPdata.loc[UPdata.index[x], 'refined_pb'] = UPdata["log_pb"].iloc[x]
    else:
        UPdata.loc[UPdata.index[x], 'refined_pb'] = np.nan





UPdata = UPdata.dropna(subset=['Beta', 'Price to Book', 'Z-Score'])





std_refbeta = UPdata['refined_beta'].std()
mean_refbeta = UPdata['refined_beta'].mean()
std_refpb = UPdata['refined_pb'].std()
mean_refpb = UPdata['refined_pb'].mean()




for x in range(len(UPdata.index)):
        UPdata.loc[UPdata.index[x], 'z-score_beta'] = (UPdata["Beta"].iloc[x] - mean_refbeta)/std_refbeta
        UPdata.loc[UPdata.index[x], 'z-score_pb'] = (math.log(UPdata["Price to Book"].iloc[x], 10) - mean_refpb)/std_refpb





for x in range(len(UPdata.index)):
        UPdata.loc[UPdata.index[x], 'sum z-score'] = (UPdata["z-score_beta"].iloc[x] + UPdata["z-score_pb"].iloc[x] +UPdata["Z-Score"].iloc[x])





UPdata.sort_values(by=['sum z-score'], inplace=True)





sum_topten = 0
for x in range(9):
    sum_topten = UPdata["sum z-score"].iloc[x] + sum_topten
    UPdata.loc[UPdata.index[x], 'position']  = "Long"
weightage_eachtop = 0.5/sum_topten





sum_bottomten = 0
for x in range(1,10):
    xmodi = x * (-1)
    sum_bottomten = UPdata["sum z-score"].iloc[xmodi] + sum_bottomten
    UPdata.loc[UPdata.index[xmodi], 'position'] = "Short"
    
weightage_eachbottom = 0.5/sum_bottomten





for x in range(9):
    UPdata.loc[UPdata.index[x], 'weightage %']  = UPdata["sum z-score"].iloc[x] * weightage_eachtop
    UPdata.loc[UPdata.index[x], 'avg z-score'] = (UPdata['sum z-score'].iloc[x])/3





for x in range(1,10):
    xmodi = x * (-1)  
    UPdata.loc[UPdata.index[xmodi], 'weightage %'] = UPdata["sum z-score"].iloc[xmodi] * weightage_eachbottom
    UPdata.loc[UPdata.index[xmodi], 'avg z-score'] = (UPdata['sum z-score'].iloc[xmodi])/3





UPdata = UPdata.dropna(subset=['weightage %'])





UPdata = UPdata.drop(['Beta', 'Price to Book', 'Z-Score','refined_beta', 'refined_pb', 'log_pb','z-score_beta', 'z-score_pb', 'sum z-score'], axis=1)




def color_negative_red(value):
    if value == 'Short':
        color = 'red'

    else:
        color = 'green'
        
        
    return 'color: %s' % color

(UPdata.style
    .applymap(color_negative_red, subset=['position'])
    .format({'weightage %': "{:.2%}"}))




UPdata.to_csv ('dollar nuetral portfolio.csv', index = False, header=True)


# In[ ]:





# In[ ]:





# In[ ]:




