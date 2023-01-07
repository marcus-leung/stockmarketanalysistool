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

    def __init__(self, ticker, interval='5', high=False, low=False, SMA=None):
        self.ticker = ticker
        self.interval = interval
        self.outputsize = 'full'
        self.high = high
        self.low = low
        self.SMA = SMA

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
        SMA = []
        market_open_time = datetime.strptime('09:30:00', '%H:%M:%S')
        market_close_time = datetime.strptime('16:00:00', '%H:%M:%S')
        for i, date in enumerate(time_series):
            time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if i == 0:
                curr_day = time.strftime('%Y-%m-%d')
            if i > 0 and time.strftime('%Y-%m-%d') != curr_day: break

            if time.time() >= market_open_time.time() and time.time() <= market_close_time.time():
                time = time.strftime('%I:%M:%S') 
                times.append(time)
                close_vals.append(float(time_series[date]['4. close']))
                high_vals.append(float(time_series[date]['2. high']))
                low_vals.append(float(time_series[date]['3. low']))

        if self.SMA is not None:
            for i in range(len(close_vals)-self.SMA+1):
                total_over_period = close_vals[i:i+self.SMA] 
                curr_SMA = sum(total_over_period)/self.SMA
                SMA.append(round(curr_SMA, 2))

        fig, ax = plt.subplots()
        plt.ion()

        times = times[::-1]
        close_vals = close_vals[::-1]
        high_vals = high_vals[::-1]
        low_vals = low_vals[::-1]

        ax.plot(times, close_vals, label='Close', color='blue')
        if self.high: ax.plot(times, high_vals, label='High', color='green')
        if self.low: ax.plot(times, low_vals, label='Close', color='red')
        if self.SMA: ax.plot(times[self.SMA-1:], SMA[::-1], label=f'{self.SMA} SMA', color='orange')
        
        if self.interval == '60':
            ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
        else:
            ax.xaxis.set_major_locator(MaxNLocator(nbins=20))

        ax.set_xlabel(f'Time ({self.interval} min)')
        ax.set_ylabel('Close Price')
        ax.set_title(f'Stock Price Over Time ({curr_day})')
        
        ax.legend()
        plt.grid()
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
        SMA = []
        for i, date in enumerate(time_series):
            if i == 50: break #Number of data inputs
            time = datetime.strptime(date, '%Y-%m-%d')
            times.append(time)
            close_vals.append(float(time_series[date]['4. close']))
            high_vals.append(float(time_series[date]['2. high']))
            low_vals.append(float(time_series[date]['3. low']))   


        if self.SMA is not None:
            for i in range(len(close_vals)-self.SMA+1):
                total_over_period = close_vals[i:i+self.SMA]
                curr_SMA = sum(total_over_period)/self.SMA
                SMA.append(round(curr_SMA, 2))


        fig, ax = plt.subplots()
        plt.ion()

        ax.plot(times, close_vals, label='Close', color='blue')
        if self.high: ax.plot(times, high_vals, label='High', color='green')
        if self.low: ax.plot(times, low_vals, label='Close', color='red')
        if self.SMA: ax.plot(times[:len(times)-self.SMA+1], SMA, label=f'{self.SMA} SMA', color='orange')

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
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
