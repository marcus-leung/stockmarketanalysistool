import requests
import os

api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

class DataGetter:
    def __init__(self, ticker, function='TIME_SERIES_INTRADAY', interval='5'):
        self.ticker = ticker
        self.function = function
        self.interval = interval
        self.outputsize = 'compact'

    def getJSON(self):
        response = requests.get(f'https://www.alphavantage.co/query?function={self.function}&symbol={self.ticker}&interval={self.interval}min&apikey={api_key}&outputsize={self.outputsize}')
        return response.json() #dict

