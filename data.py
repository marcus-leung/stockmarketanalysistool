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

    def __init__(self, ticker, interval='5', high=False, low=False, SMA=None, EMA=None, fib=False):
        self.ticker = ticker
        self.interval = interval
        self.outputsize = 'full'
        self.high = high
        self.low = low
        self.SMA = SMA
        self.EMA = EMA
        self.fib = fib

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
            SMA = self.calc_SMA(close_vals, self.SMA)

        if self.EMA is not None:
            EMA = self.calc_EMA(close_vals, self.EMA)

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
        if self.EMA: ax.plot(times[self.EMA-1:], EMA[::-1], label=f'{self.EMA} EMA', color='yellow')
        
        if self.interval == '60':
            ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
        else:
            ax.xaxis.set_major_locator(MaxNLocator(nbins=20))

        ax.set_xlabel(f'Time ({self.interval} min)')
        ax.set_ylabel('Close Price')
        ax.set_title(f'Stock Price Over Time ({curr_day})')
        ax.legend()

        if self.fib:
            for v in self.calc_fib_retra_lvls(close_vals):
                plt.axhline(y=v, color='black', linestyle='dashed')

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
            SMA = self.calc_SMA(close_vals, self.SMA)

        if self.EMA is not None:
            EMA = self.calc_EMA(close_vals, self.EMA)

        fig, ax = plt.subplots()
        plt.ion()

        ax.plot(times, close_vals, label='Close', color='blue')
        if self.high: ax.plot(times, high_vals, label='High', color='green')
        if self.low: ax.plot(times, low_vals, label='Close', color='red')
        if self.SMA: ax.plot(times[:len(times)-self.SMA+1], SMA, label=f'{self.SMA} SMA', color='orange')
        if self.EMA: ax.plot(times[:len(times)-self.EMA+1], EMA, label=f'{self.EMA} EMA', color='yellow')

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

        if self.fib:
            for v in self.calc_fib_retra_lvls(close_vals):
                plt.axhline(y=v, color='black', linestyle='dashed')

        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def calc_SMA(self, vals, period):
        SMA = []
        for i in range(len(vals)-period+1):
            total_over_period = vals[i:i+self.SMA] 
            curr_SMA = sum(total_over_period)/self.SMA
            SMA.append(round(curr_SMA, 2))

        return SMA

    def calc_EMA(self, vals, period, smoothing_val=2):
        EMA = []
        EMA.append(sum(vals[:period]) / period) #append SMA of days as first value
        
        for val in vals[period:]:
            ema_val = (val * (smoothing_val/(1 + period))) + EMA[-1] * (1 - (smoothing_val / (1 + period)))
            EMA.append(ema_val)

        return EMA

    def calc_fib_retra_lvls(self, vals):
        levels = []
        lowest = vals[0]
        highest = vals[0]
        for val in vals:
            if val > highest: highest = val
            if val < lowest: lowest = val

        difference = highest - lowest
        levels.append(lowest)
        levels.append(lowest + (difference * 0.236)) 
        levels.append(lowest + (difference * 0.382))
        levels.append(lowest + (difference * 0.5))
        levels.append(lowest + (difference * 0.618))
        levels.append(lowest + (difference * 0.764))
        levels.append(highest)

        return levels #returns list of levels in order of 0%, 23.6%, 38.2%, 50%, 61.8%, 76.4%, 100%
        