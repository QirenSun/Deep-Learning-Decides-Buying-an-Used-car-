# run this  !pip install pandas_datareader
from pandas_datareader import data as web
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def get_stock(ticker, start_date, end_date, s_window, l_window):
    try:
        df = web.get_data_yahoo(ticker, start=start_date, end=end_date)
        df['Return'] = df['Adj Close'].pct_change()
        df['Return'].fillna(0, inplace = True)
        df['Date'] = df.index
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year 
        df['Day'] = df['Date'].dt.day
        df['Weekday'] = df['Date'].dt.weekday_name  
        df['Short_MA'] = df['Adj Close'].rolling(window=s_window, min_periods=1).mean()
        df['Long_MA'] = df['Adj Close'].rolling(window=l_window, min_periods=1).mean()        
        col_list = ['Date', 'Year', 'Month', 'Day', 'Weekday',
                    'High', 'Low', 'Close', 'Volume', 'Adj Close',
                    'Return', 'Short_MA', 'Long_MA']
        df = df[col_list]
        return df
    except Exception as error:
        print(error)
        return None

ticker='S'
start_date='2014-01-01'
end_date='2019-01-01'
s_window = 10
l_window = 80
input_dir = 'C:\\Users\\Administrator\\Desktop\\Python_data'
output_file = os.path.join(input_dir, ticker + '.csv')

df = get_stock(ticker, start_date, end_date, s_window, l_window)
df.to_csv(output_file, index=False)


with open(output_file) as f:
    lines = f.read().splitlines()




def year_pro_a1(year):    
    retu=np.array(df['Return'])
    #adj_close=np.array([df['Adj Close']])
    buy=np.where(retu <=0,retu,1)
    naive=np.where(buy>=0,buy,-1)
    sum_year=0
    for i in range(len(df)):
        if df['Year'][i]==year:
            sum_year+=1
            last_day=i
    
    profit=0
    num=0
    for i in range(last_day-sum_year+1,last_day):
        if naive[i]== naive[i+1] and naive[i+1]==-1:
            profit+=float(format(100/df['Adj Close'][i+1],'0.2f'))
            num-=1
            last_adj=df['Adj Close'][i+1]
        elif naive[i]== naive[i+1] and  naive[i+1]==1:
            #profit+=float(format(-100/df['Adj Close'][i],'0.2f'))
            last_adj=df['Adj Close'][i]
            #num+=1
        else:
            last_adj=df['Adj Close'][i]
    profit_year=float(format(profit*last_adj+num*100,'0.2f'))    
    return profit_year    

year=[year_pro_a1(2014),year_pro_a1(2015),year_pro_a1(2016),year_pro_a1(2017),year_pro_a1(2018)]
print(year)

























