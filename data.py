import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import pandas as pd
import os
from datetime import datetime

api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

class DataGetter:
    functions = {
        'INTRADAY':'TIME_SERIES_INTRADAY',
        'DAILY':'TIME_SERIES_DAILY_ADJUSTED',
        'WEEKLY':'TIME_SERIES_WEEKLY',
        'MONTHLY':'TIME_SERIES_MONTHLY'
    }

    interval_names = {
        '1':'Time Series (1min)',
        '5':'Time Series (5min)',
        '15':'Time Series (15min)',
        '30':'Time Series (30min)',
        '60':'Time Series (60min)',
        'Daily':'Time Series (Daily)',
        'Weekly':'Weekly Time Series',
        'Monthly':'Monthly Time Series'
    }

    def __init__(self, ticker, interval='5', high=False, low=False):
        self.ticker = ticker
        self.interval = interval
        self.outputsize = 'compact'
        self.high = high
        self.low = low

        if interval == 'DAILY' or interval == 'WEEKLY' or interval == 'MONTHLY':
            self.function = self.functions[interval]
            self.interval = '5'
        else:
            self.function = self.functions['INTRADAY']

    def getJSON(self):
        response = requests.get(f'https://www.alphavantage.co/query?function={self.function}&symbol={self.ticker}&interval={self.interval}min&apikey={api_key}&outputsize={self.outputsize}')
        return response.json() #dict

    def showPlot(self):
        if self.function == self.functions['INTRADAY']:
            self.show_Plot_Intraday()
        else:
            self.show_Plot_Other()

    def show_Plot_Intraday(self): 
        response = self.getJSON()

        time_series = response[self.interval_names[self.interval]]

        times = []
        close_vals = []
        high_vals = []
        low_vals = []
        for i, date in enumerate(time_series):
            time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if i == 0:
                curr_day = time.strftime('%Y-%m-%d')
            if i > 0 and time.strftime('%Y-%m-%d') != curr_day: break
            time = time.strftime('%H:%M:%S')
            times.append(time)
            close_vals.append(float(time_series[date]['4. close']))
            high_vals.append(float(time_series[date]['2. high']))
            low_vals.append(float(time_series[date]['3. low']))            

        fig, ax = plt.subplots()

        ax.plot(times, close_vals, label='Close', color='blue')
        if self.high: ax.plot(times, high_vals, label='High', color='green')
        if self.low: ax.plot(times, low_vals, label='Close', color='red')
        ax.xaxis.set_major_locator(MaxNLocator(nbins=25))

        ax.set_xlabel(f'Time ({self.interval} min)')
        ax.set_ylabel('Close Price')
        ax.set_title(f'Stock Price Over Time ({curr_day})')
        
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_Plot_Other(self): #dict
        response = self.getJSON()

        if self.function == self.functions['DAILY']:
            time_series = response[self.interval_names['Daily']] 
        elif self.function == self.functions['WEEKLY']:
            time_series = response[self.interval_names['Weekly']] 
        else:
            time_series = response[self.interval_names['Monthly']] 

        times = []
        close_vals = []
        high_vals = []
        low_vals = []
        for i, date in enumerate(time_series):
            if i == 50: break #Number of data inputs
            time = datetime.strptime(date, '%Y-%m-%d')
            times.append(time)
            close_vals.append(float(time_series[date]['4. close']))
            high_vals.append(float(time_series[date]['2. high']))
            low_vals.append(float(time_series[date]['3. low']))   

        fig, ax = plt.subplots()

        ax.plot(times, close_vals, label='Close', color='blue')
        if self.high: ax.plot(times, high_vals, label='High', color='green')
        if self.low: ax.plot(times, low_vals, label='Close', color='red')
        ax.xaxis.set_major_locator(MaxNLocator(nbins=20))

        ax.set_xlabel('Time')
        if self.function == self.functions['DAILY']:
            ax.set_xlabel(f'Time (Daily)')
        elif self.function == self.functions['WEEKLY']:
            ax.set_xlabel(f'Time (Weekly)')
        else:
            ax.set_xlabel(f'Time (Montly)')
        ax.set_ylabel('Close Price')
        ax.set_title(f'Stock Price Over Time')

        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
