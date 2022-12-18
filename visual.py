import matplotlib.pyplot as plt
import pandas as pd

def showPlot(response): #dict

    time_series = response['Time Series (5min)']

    dates = []
    values = []
    for date in time_series:
        dates.append(date)
        values.append(float(time_series[date]['4. close']))

    plt.plot(dates, values)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Price Over Time')
    plt.xticks(rotation=45)
    plt.show()
